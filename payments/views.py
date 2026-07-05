import uuid
import requests

from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import (
    IsFinance,
    IsAdmin
)

from employees.models import Employee
from payroll.models import SalaryTransaction
from logs.models import AuditLog

from .services import PaymentService


class ProcessAllPaymentsView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsFinance
    ]

    def post(self, request):

        transactions = (
            SalaryTransaction.objects.filter(
                status="Pending"
            )
        )

        if not transactions.exists():

            return Response(
                {
                    "status": False,
                    "message":
                    "No pending transactions found"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        results = []

        for transaction in transactions:

            employee = transaction.employee
            reference = str(uuid.uuid4())

            if not employee.recipient_code:

                transaction.status = "Failed"
                transaction.failure_reason = (
                    "Recipient code missing"
                )
                transaction.reference = reference
                transaction.save()

                AuditLog.objects.create(
                    user=request.user,
                    action="Bulk payment failed",
                    details=f"{employee.full_name}: Recipient missing"
                )

                results.append({
                    "employee":
                    employee.full_name,
                    "status":
                    "Failed",
                    "reason":
                    "Recipient missing"
                })

                continue

            try:

                response = (
                    PaymentService.initiate_transfer(
                        amount=transaction.amount,
                        recipient_code=employee.recipient_code,
                        reference=reference
                    )
                )

                transaction.reference = reference

                if response.get("status"):

                    transaction.status = "Success"

                    transaction.paystack_reference = (
                        response.get(
                            "data",
                            {}
                        ).get(
                            "reference",
                            reference
                        )
                    )

                    transaction.failure_reason = None

                    AuditLog.objects.create(
                        user=request.user,
                        action="Bulk payment processed",
                        details=f"{employee.full_name}"
                    )

                else:

                    transaction.status = "Failed"

                    transaction.failure_reason = (
                        response.get(
                            "message",
                            "Transfer failed"
                        )
                    )

                    AuditLog.objects.create(
                        user=request.user,
                        action="Bulk payment failed",
                        details=(
                            f"{employee.full_name}: "
                            f"{transaction.failure_reason}"
                        )
                    )

                transaction.save()

                results.append({
                    "employee":
                    employee.full_name,
                    "status":
                    transaction.status
                })

            except Exception as e:

                transaction.status = "Failed"
                transaction.failure_reason = str(e)
                transaction.reference = reference
                transaction.save()

                AuditLog.objects.create(
                    user=request.user,
                    action="Bulk payment exception",
                    details=str(e)
                )

                results.append({
                    "employee":
                    employee.full_name,
                    "status":
                    "Failed",
                    "reason":
                    str(e)
                })

        return Response(
            {
                "status": True,
                "processed": len(results),
                "results": results
            },
            status=status.HTTP_200_OK
        )


class TestPaystackView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get(self, request):

        headers = {
            "Authorization":
            f"Bearer {settings.PAYSTACK_SECRET_KEY}"
        }

        try:

            response = requests.get(
                "https://api.paystack.co/bank",
                headers=headers,
                timeout=30
            )

            AuditLog.objects.create(
                user=request.user,
                action="Paystack API tested"
            )

            return Response(
                response.json(),
                status=response.status_code
            )

        except requests.exceptions.RequestException as e:

            return Response(
                {
                    "status": False,
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateRecipientView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsFinance
    ]

    def post(self, request, employee_id):

        employee = get_object_or_404(
            Employee,
            id=employee_id
        )

        response = (
            PaymentService.create_recipient(
                employee
            )
        )

        if response.get("status"):

            employee.recipient_code = (
                response["data"][
                    "recipient_code"
                ]
            )

            employee.save()

            AuditLog.objects.create(
                user=request.user,
                action="Recipient created",
                details=employee.full_name
            )

            return Response(
                response,
                status=status.HTTP_200_OK
            )

        return Response(
            response,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProcessPaymentView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsFinance
    ]

    def post(
        self,
        request,
        transaction_id
    ):

        transaction = get_object_or_404(
            SalaryTransaction,
            id=transaction_id
        )

        employee = transaction.employee

        if not employee.recipient_code:

            return Response(
                {
                    "status": False,
                    "message":
                    "Recipient code not found"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        reference = str(uuid.uuid4())

        try:

            response = (
                PaymentService.initiate_transfer(
                    amount=transaction.amount,
                    recipient_code=employee.recipient_code,
                    reference=reference
                )
            )

            transaction.reference = reference

            if response.get("status"):

                transaction.status = "Success"

                AuditLog.objects.create(
                    user=request.user,
                    action="Salary processed",
                    details=employee.full_name
                )

            else:

                transaction.status = "Failed"

                transaction.failure_reason = (
                    response.get(
                        "message"
                    )
                )

                AuditLog.objects.create(
                    user=request.user,
                    action="Salary failed",
                    details=(
                        f"{employee.full_name}: "
                        f"{transaction.failure_reason}"
                    )
                )

            transaction.save()

            return Response(
                response,
                status=status.HTTP_200_OK
            )

        except Exception as e:

            transaction.status = "Failed"
            transaction.failure_reason = str(e)
            transaction.save()

            AuditLog.objects.create(
                user=request.user,
                action="Payment exception",
                details=str(e)
            )

            return Response(
                {
                    "status": False,
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )