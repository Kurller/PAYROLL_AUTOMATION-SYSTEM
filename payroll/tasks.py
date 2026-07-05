# payroll/tasks.py

from celery import shared_task

from .models import SalaryTransaction
from payments.services import PaymentService


@shared_task
def process_salary_batch(batch_id):

    transactions = (
        SalaryTransaction.objects.filter(
            batch_id=batch_id
        )
    )

    for transaction in transactions:

        employee = transaction.employee

        if employee.recipient_code:

            PaymentService.initiate_transfer(
                amount=transaction.amount,
                recipient_code=employee.recipient_code,
                reference=transaction.reference
            )