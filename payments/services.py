import requests
import certifi

from django.conf import settings


class PaymentService:

    BASE_URL = "https://api.paystack.co"

    @classmethod
    def create_recipient(cls, employee):

        if not employee.bank_code:
            return {
                "status": False,
                "message": "Bank code is required"
            }

        if not employee.account_number:
            return {
                "status": False,
                "message": "Account number is required"
            }

        headers = {
            "Authorization":
            f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "type": "nuban",
            "name": employee.full_name,
            "account_number": employee.account_number,
            "bank_code": employee.bank_code,
            "currency": "NGN"
        }

        try:

            print("Recipient payload:", payload)

            response = requests.post(
                f"{cls.BASE_URL}/transferrecipient",
                json=payload,
                headers=headers,
                verify=certifi.where(),
                timeout=30
            )

            data = response.json()

            print("Recipient response:", data)

            return data

        except requests.exceptions.RequestException as e:

            return {
                "status": False,
                "message": str(e)
            }

    @classmethod
    def initiate_transfer(
        cls,
        amount,
        recipient_code,
        reference
    ):

        # Development mode (bypass Paystack transfer)
        if settings.DEBUG:

            return {
                "status": True,
                "message": "Mock transfer successful",
                "data": {
                    "reference": reference,
                    "recipient": recipient_code,
                    "amount": float(amount)
                }
            }

        headers = {
            "Authorization":
            f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "source": "balance",
            "amount": int(float(amount) * 100),
            "recipient": recipient_code,
            "reason": "Salary payment",
            "reference": reference
        }

        try:

            print("Transfer payload:", payload)

            response = requests.post(
                f"{cls.BASE_URL}/transfer",
                json=payload,
                headers=headers,
                verify=certifi.where(),
                timeout=30
            )

            data = response.json()

            print("Transfer response:", data)

            return data

        except requests.exceptions.RequestException as e:

            return {
                "status": False,
                "message": str(e)
            }