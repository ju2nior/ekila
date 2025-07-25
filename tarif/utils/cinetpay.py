import os
import uuid
from typing import Dict
from typing import Literal

import requests
from dotenv import load_dotenv

load_dotenv()


class CinetPay:
    BASE_URL = "https://api-checkout.cinetpay.com/v2"

    def __init__(self):
        self.api_key: str = os.getenv("CINETPAY_API_KEY")
        self.site_id: str = os.getenv("CINETPAY_SITE_ID")
        self.host = os.getenv("HOST")
        self.notify_url = f"https://{self.host}/offres/notify-orders/"
        self.return_url = f"https://{self.host}/offres/success-orders/"
        self.headers: Dict[str, str] = {"Content-Type": "application/json"}

    def initiate_payment(
        self,
        amount: int,
        customer_name: str,
        customer_email: str,
        customer_phone: str,
        currency: Literal["XAF", "XOF", "CDF"] = "XAF",
        description: str = "Paiement en ligne",
    ) -> Dict[str, str]:
        transaction_id = str(uuid.uuid4())
        payload = {
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_phone_number": customer_phone,
            "description": description,
            "site_id": self.site_id,
            "apikey": self.api_key,
            "notify_url": self.notify_url,
            "return_url": self.return_url,
            "channels": "ALL",
            "metadata": "Paiement Django",
        }

        try:
            response = requests.post(
                f"{self.BASE_URL}/payment",
                json=payload,
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()

            data = response.json()

            if data.get("code") == "201":
                return {
                    "payment_url": data["data"]["payment_url"],
                    "transaction_id": transaction_id,
                }
            else:
                raise Exception(
                    f"Erreur CinetPay: {data.get('message', 'Erreur inconnue')}"
                )

        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors de la requête vers CinetPay : {str(e)}")

        except ValueError:
            raise Exception("Réponse invalide reçue de CinetPay (JSON malformé).")

    def verify_payment(self, transaction_id: str) -> Dict:
        payload = {
            "transaction_id": transaction_id,
            "site_id": self.site_id,
            "apikey": self.api_key,
        }

        try:
            response = requests.post(
                f"{self.BASE_URL}/payment/check", json=payload, headers=self.headers
            )
            data = response.json()

            if response.status_code != 200:
                raise Exception(f"Erreur HTTP {response.status_code} : {response.text}")

            if data.get("code") != "00":
                raise Exception(
                    f"Vérification échouée : {data.get('message', 'Erreur inconnue')}"
                )

            return data

        except requests.RequestException as e:
            raise Exception(
                f"Erreur réseau lors de la vérification du paiement : {str(e)}"
            )

        except ValueError:
            raise Exception("Réponse invalide du serveur de CinetPay.")
