from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tarif.models import AdvertisingOffer
from tarif.models import Order
from tarif.models import Payment
from tarif.models import PaymentStatus


class CinetPayTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.offer = AdvertisingOffer.objects.create(
            name="Offre Test",
            unit_price=1000,
            is_active=True,
            is_visible=True,
            support_type="audio",
        )

        self.order = Order.objects.create(
            reference="TEST123",
            description="Commande de test",
            amount=1000,
            cart=[
                {
                    "id": self.offer.id,
                    "name": self.offer.name,
                    "unit_price": self.offer.unit_price,
                    "quantity": 1,
                }
            ],
            user=self.user,
        )

    def test_initiate_payment_success(self):
        with patch("tarif.utils.cinetpay.CinetPay.initiate_payment") as mock_initiate:
            mock_initiate.return_value = {
                "payment_url": "https://payment.example.com",
                "transaction_id": "CP123456789",
            }

            response = self.client.post(
                reverse("order-create-payment", kwargs={"pk": self.order.id})
            )

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data["transaction_id"], "CP123456789")
            self.assertEqual(
                response.data["payment_url"], "https://payment.example.com"
            )

            payment = Payment.objects.get(order=self.order)
            self.assertEqual(payment.transaction_id, "CP123456789")
            self.assertEqual(payment.status, PaymentStatus.PENDING)

    def test_initiate_payment_already_exists(self):
        Payment.objects.create(
            order=self.order,
            transaction_id="EXISTING123",
            amount=1000,
            status=PaymentStatus.PENDING,
        )

        response = self.client.post(
            reverse("order-create-payment", kwargs={"pk": self.order.id})
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Un paiement existe déjà pour cette commande"
        )

    def test_cinetpay_callback_success(self):
        payment = Payment.objects.create(
            order=self.order,
            transaction_id="CALLBACK_TEST",
            amount=1000,
            status=PaymentStatus.PENDING,
        )

        with patch("tarif.utils.cinetpay.CinetPay.verify_payment") as mock_verify:
            mock_verify.return_value = {
                "code": "00",
                "data": {
                    "status": PaymentStatus.ACCEPTED,
                    "metadata": {"order_id": self.order.id},
                },
            }

            response = self.client.post(
                reverse("payment-callback"),
                data={
                    "cpm_trans_id": "CALLBACK_TEST",
                    "cpm_result": "00",
                    "signature": "valid_signature",
                },
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["new_status"], PaymentStatus.ACCEPTED)

            payment.refresh_from_db()
            self.order.refresh_from_db()

            self.assertEqual(payment.status, PaymentStatus.ACCEPTED)
            self.assertTrue(self.order.is_paid)

    def test_cinetpay_callback_failed(self):
        payment = Payment.objects.create(
            order=self.order,
            transaction_id="CALLBACK_FAIL",
            amount=1000,
            status=PaymentStatus.PENDING,
        )

        with patch("tarif.utils.cinetpay.CinetPay.verify_payment") as mock_verify:
            mock_verify.return_value = {
                "code": "00",
                "data": {
                    "status": PaymentStatus.REFUSED,
                    "message": "Solde insuffisant",
                },
            }

            response = self.client.post(
                reverse("payment-callback"),
                data={
                    "cpm_trans_id": "CALLBACK_FAIL",
                    "cpm_result": "03",
                    "cpm_error_message": "Solde insuffisant",
                },
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            payment.refresh_from_db()
            self.assertEqual(payment.status, PaymentStatus.REFUSED)
            self.assertFalse(self.order.is_paid)

    def test_manual_payment_verification_success(self):
        payment = Payment.objects.create(
            order=self.order,
            transaction_id="MANUAL_VERIFY",
            amount=1000,
            status=PaymentStatus.PENDING,
        )

        with patch("tarif.utils.cinetpay.CinetPay.verify_payment") as mock_verify:
            mock_verify.return_value = {
                "code": "00",
                "data": {"status": PaymentStatus.ACCEPTED},
            }

            response = self.client.post(
                reverse("payment-verify", kwargs={"pk": payment.id})
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["status"], PaymentStatus.ACCEPTED)

            payment.refresh_from_db()
            self.order.refresh_from_db()
            self.assertEqual(payment.status, PaymentStatus.ACCEPTED)
            self.assertTrue(self.order.is_paid)

    def test_manual_payment_verification_failed(self):
        payment = Payment.objects.create(
            order=self.order,
            transaction_id="VERIFY_FAIL",
            amount=1000,
            status=PaymentStatus.PENDING,
        )

        with patch("tarif.utils.cinetpay.CinetPay.verify_payment") as mock_verify:
            mock_verify.return_value = {
                "code": "05",
                "message": "Échec de la vérification",
            }

            response = self.client.post(
                reverse("payment-verify", kwargs={"pk": payment.id})
            )

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(
                response.data["error"], "Échec de la vérification du paiement"
            )

    def test_cinetpay_api_failure(self):
        with patch("tarif.utils.cinetpay.CinetPay.initiate_payment") as mock_initiate:
            mock_initiate.side_effect = Exception("API timeout")

            response = self.client.post(
                reverse("order-create-payment", kwargs={"pk": self.order.id})
            )

            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            self.assertEqual(response.data["error"], "Erreur interne du serveur")

    def test_callback_payment_not_found(self):
        response = self.client.post(
            reverse("payment-callback"), data={"cpm_trans_id": "INVALID_TRANSACTION"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Paiement non trouvé")

    def test_verify_payment_wrong_user(self):
        other_user = User.objects.create_user(
            username="otheruser", password="otherpassword"
        )

        other_order = Order.objects.create(
            reference="OTHER_ORDER", amount=500, user=other_user
        )
        payment = Payment.objects.create(
            order=other_order, transaction_id="OTHER_PAYMENT", amount=500
        )

        response = self.client.post(
            reverse("payment-verify", kwargs={"pk": payment.id})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
