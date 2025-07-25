import logging
import uuid

from django.contrib.auth import login
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from tarif.models import AdPlacement
from tarif.models import AdvertisingOffer
from tarif.models import OfferCategory
from tarif.models import OfferOption
from tarif.models import Order
from tarif.models import Payment
from tarif.models import PaymentStatus
from tarif.serializers import AdPlacementSerializer
from tarif.serializers import AdvertisingOfferSerializer
from tarif.serializers import LoginSerializer
from tarif.serializers import OfferCategorySerializer
from tarif.serializers import OfferOptionSerializer
from tarif.serializers import OrderSerializer
from tarif.serializers import PaymentSerializer
from tarif.serializers import RegisterSerializer
from tarif.serializers import UserSerializer
from tarif.utils.cinetpay import CinetPay

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response("Utilisateur créé", UserSerializer),
            400: openapi.Response("Erreur de validation"),
        },
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response("Utilisateur connecté", UserSerializer),
            400: openapi.Response("Identifiants invalides"),
        },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        request._dont_enforce_csrf_checks = True
        return super().dispatch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Déconnexion de l'utilisateur",
        responses={
            200: openapi.Response(
                "Succès",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            )
        },
    )
    def post(self, request):
        logout(request)
        return Response({"detail": "Déconnexion réussie"}, status=status.HTTP_200_OK)


class UserProfileView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={200: UserSerializer},
        operation_description="Obtenir les informations du profil utilisateur",
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Mettre à jour le profil de l'utilisateur",
        request_body=UserSerializer,
        responses={200: UserSerializer, 400: openapi.Response("Erreur de validation")},
    )
    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferCategoryViewSet(viewsets.ModelViewSet):
    queryset = OfferCategory.objects.all()
    serializer_class = OfferCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]


class AdvertisingOfferViewSet(viewsets.ModelViewSet):
    queryset = AdvertisingOffer.objects.filter(is_active=True, is_visible=True)
    serializer_class = AdvertisingOfferSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "support_type"]

    @action(detail=True, methods=["get"])
    def options(self, request, pk=None):
        offer = self.get_object()
        options = offer.options.all()
        serializer = OfferOptionSerializer(options, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def placements(self, request, pk=None):
        offer = self.get_object()
        placements = offer.placements.all()
        serializer = AdPlacementSerializer(placements, many=True)
        return Response(serializer.data)


class OfferOptionViewSet(viewsets.ModelViewSet):
    queryset = OfferOption.objects.all()
    serializer_class = OfferOptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["offer"]


class AdPlacementViewSet(viewsets.ModelViewSet):
    queryset = AdPlacement.objects.all()
    serializer_class = AdPlacementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["offer", "available_slots"]


@method_decorator(csrf_exempt, name="dispatch")
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        request._dont_enforce_csrf_checks = True
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Order.objects.none()
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = serializer.validated_data.get("cart", [])
        if not cart:
            return Response(
                {"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        total = sum(item["unit_price"] * item["quantity"] for item in cart)

        reference = str(uuid.uuid4()).replace("-", "")[:15]
        order = Order.objects.create(
            reference=reference,
            description=f"Commande de {request.user.username}",
            amount=total,
            cart=cart,
            user=request.user,
        )

        response_serializer = self.get_serializer(order)
        headers = self.get_success_headers(response_serializer.data)

        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=True, methods=["post"])
    def create_payment(self, request, pk=None):
        try:
            order = self.get_object()

            if hasattr(order, "payment"):
                return Response(
                    {"error": "Un paiement existe déjà pour cette commande"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            cp = CinetPay()
            payment_response = cp.initiate_payment(
                amount=order.amount,
                customer_name=request.user.get_full_name() or request.user.username,
                customer_email=request.user.email,
                customer_phone="237612345678",
                description=f"Paiement de la commande {order.reference}",
            )

            payment = Payment.objects.create(
                order=order,
                transaction_id=payment_response["transaction_id"],
                amount=order.amount,
                status=PaymentStatus.PENDING,
            )

            return Response(
                {
                    "payment_id": payment.id,
                    "transaction_id": payment.transaction_id,
                    "payment_url": str(payment_response["payment_url"]),
                    "message": "Paiement initialisé avec succès",
                },
                status=status.HTTP_201_CREATED,
            )

        except Order.DoesNotExist:
            return Response(
                {"error": "Commande introuvable"}, status=status.HTTP_404_NOT_FOUND
            )
        except KeyError as e:
            logger.error(f"Erreur dans la réponse CinetPay: {str(e)}")
            return Response(
                {"error": "Réponse invalide de CinetPay", "detail": str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        except Exception as e:
            logger.exception("Erreur inattendue lors de la création du paiement")
            return Response(
                {"error": "Erreur interne du serveur", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        request._dont_enforce_csrf_checks = True
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Payment.objects.none()
        return Payment.objects.filter(order__user=self.request.user)

    @action(detail=True, methods=["post"])
    def verify(self, request, pk=None):
        payment = self.get_object()

        cp = CinetPay()
        result = cp.verify_payment(payment.transaction_id)

        if result.get("code") == "00":
            new_status = result["data"]["status"]
            payment.status = new_status
            payment.response_data = result["data"]
            payment.save()

            if new_status == PaymentStatus.ACCEPTED:
                payment.order.is_paid = True
                payment.order.save()

            return Response(
                {"status": new_status, "message": "Statut de paiement mis à jour"}
            )

        return Response(
            {"error": "Échec de la vérification du paiement"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class OfferListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        offers = AdvertisingOffer.objects.filter(is_active=True, is_visible=True)
        serializer = AdvertisingOfferSerializer(offers, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name="dispatch")
class CartAPIView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_description="Obtenir le contenu du panier",
        responses={200: openapi.Response("Liste des items du panier")},
    )
    def dispatch(self, request, *args, **kwargs):
        if isinstance(request, Request):
            request = request._request

        setattr(request, "_dont_enforce_csrf_checks", True)
        return super().dispatch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obtenir le contenu du panier",
        responses={
            200: openapi.Response(
                "Panier",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "name": openapi.Schema(type=openapi.TYPE_STRING),
                            "unit_price": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "quantity": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "support_type": openapi.Schema(type=openapi.TYPE_STRING),
                            "start_date": openapi.Schema(
                                type=openapi.TYPE_STRING, format="date"
                            ),
                            "end_date": openapi.Schema(
                                type=openapi.TYPE_STRING, format="date"
                            ),
                            "time_slot": openapi.Schema(type=openapi.TYPE_STRING),
                            "audio_choice": openapi.Schema(type=openapi.TYPE_STRING),
                        },
                    ),
                ),
            )
        },
    )
    def get(self, request, offer_id=None):
        cart = request.session.get("cart", [])
        if offer_id is None:
            return Response(cart)

        item = next((item for item in cart if item["id"] == offer_id), None)
        if item is not None:
            return Response(item)
        return Response(
            {"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND
        )

    @swagger_auto_schema(
        operation_description="Ajouter une offre au panier",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "offer_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "start_date": openapi.Schema(type=openapi.TYPE_STRING, format="date"),
                "end_date": openapi.Schema(type=openapi.TYPE_STRING, format="date"),
                "time_slot": openapi.Schema(type=openapi.TYPE_STRING),
                "audio_choice": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["offer_id"],
        ),
        responses={
            201: openapi.Response("Panier mis à jour"),
            400: openapi.Response("Erreur de validation"),
            404: openapi.Response("Offre non trouvée"),
        },
    )
    def post(self, request):
        offer_id = request.data.get("offer_id")

        if not offer_id:
            return Response(
                {"error": "offer_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            offer = AdvertisingOffer.objects.get(id=offer_id, is_active=True)
        except AdvertisingOffer.DoesNotExist:
            return Response(
                {"error": "Offer not found or inactive"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if "cart" not in request.session:
            request.session["cart"] = []

        cart = request.session["cart"]

        for item in cart:
            if item["id"] == offer_id:
                return Response(
                    {"error": "Offer already in cart"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        cart_item = {
            "id": offer.id,
            "name": offer.name,
            "unit_price": offer.unit_price,
            "quantity": 1,
            "support_type": offer.support_type,
            "start_date": request.data.get("start_date"),
            "end_date": request.data.get("end_date"),
            "time_slot": request.data.get("time_slot"),
            "audio_choice": request.data.get("audio_choice"),
        }

        cart.append(cart_item)
        request.session.modified = True
        return Response(cart, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Modifier la quantité d'une offre dans le panier",
        manual_parameters=[
            openapi.Parameter(
                "offer_id",
                openapi.IN_PATH,
                description="ID de l'offre",
                type=openapi.TYPE_INTEGER,
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "action": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=["increase", "decrease"],
                    description="Action à effectuer: 'increase' ou 'decrease'",
                )
            },
            required=["action"],
        ),
        responses={
            200: openapi.Response("Panier mis à jour"),
            400: openapi.Response("Erreur de validation"),
            404: openapi.Response("Offre non trouvée dans le panier"),
        },
    )
    def patch(self, request, offer_id=None):
        action = request.data.get("action")
        if not offer_id or not action:
            return Response(
                {"error": "offer_id and action are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = request.session.get("cart", [])
        if not cart:
            return Response(
                {"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        item_found = False
        for item in cart:
            if item["id"] == offer_id:
                item_found = True
                if action == "increase":
                    item["quantity"] += 1
                elif action == "decrease":
                    item["quantity"] -= 1
                    if item["quantity"] <= 0:
                        cart = [i for i in cart if i["id"] != offer_id]
                else:
                    return Response(
                        {"error": "Invalid action. Use 'increase' or 'decrease'"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                break

        if not item_found:
            return Response(
                {"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND
            )

        request.session["cart"] = cart
        request.session.modified = True
        return Response(cart)

    @swagger_auto_schema(
        operation_description="Retirer une offre du panier",
        manual_parameters=[
            openapi.Parameter(
                "offer_id",
                openapi.IN_PATH,
                description="ID de l'offre",
                type=openapi.TYPE_INTEGER,
            )
        ],
        responses={
            200: openapi.Response("Panier mis à jour"),
            400: openapi.Response("ID manquant"),
            404: openapi.Response("Offre non trouvée dans le panier"),
        },
    )
    def delete(self, request, offer_id=None):
        if not offer_id:
            return Response(
                {"error": "offer_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        cart = request.session.get("cart", [])
        if not cart:
            return Response(
                {"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        initial_count = len(cart)
        new_cart = [item for item in cart if item["id"] != offer_id]

        if len(new_cart) == initial_count:
            return Response(
                {"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND
            )

        request.session["cart"] = new_cart
        request.session.modified = True
        return Response(new_cart)


@method_decorator(csrf_exempt, name="dispatch")
class PaymentCallbackView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_description="Callback pour les notifications de paiement CinetPay",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "cpm_trans_id": openapi.Schema(type=openapi.TYPE_STRING),
                "cpm_amount": openapi.Schema(type=openapi.TYPE_INTEGER),
                "cpm_currency": openapi.Schema(type=openapi.TYPE_STRING),
                "signature": openapi.Schema(type=openapi.TYPE_STRING),
                "cpm_result": openapi.Schema(type=openapi.TYPE_STRING),
                "cpm_trans_date": openapi.Schema(type=openapi.TYPE_STRING),
                "cpm_phone_prefix": openapi.Schema(type=openapi.TYPE_STRING),
                "cpm_phone_number": openapi.Schema(type=openapi.TYPE_STRING),
                "cpm_custom": openapi.Schema(type=openapi.TYPE_STRING),
                "payment_method": openapi.Schema(type=openapi.TYPE_STRING),
                "cpm_error_message": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["cpm_trans_id"],
        ),
        responses={
            200: openapi.Response(
                "Succès",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING),
                        "new_status": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response("Erreur de validation"),
            404: openapi.Response("Paiement non trouvé"),
        },
    )
    def post(self, request):
        data = request.POST

        transaction_id = data.get("cpm_trans_id")
        if not transaction_id:
            return Response(
                {"error": "Transaction ID manquant"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
        except Payment.DoesNotExist:
            return Response(
                {"error": "Paiement non trouvé"}, status=status.HTTP_404_NOT_FOUND
            )

        cp = CinetPay()
        result = cp.verify_payment(transaction_id)

        if result.get("code") == "00":
            new_status = result["data"]["status"]

            payment.status = new_status
            payment.response_data = result["data"]
            payment.save()

            if new_status == PaymentStatus.ACCEPTED:
                payment.order.is_paid = True
                payment.order.save()

            return Response({"status": "success", "new_status": new_status})

        return Response(
            {
                "error": "Échec de la vérification du paiement",
                "detail": result.get("message", "Erreur inconnue"),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
