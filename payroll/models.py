from django.db import models
from employees.models import Employee
import uuid
# payroll/models.py

failure_reason = models.TextField(
    blank=True,
    null=True
)

paystack_reference = models.CharField(
    max_length=100,
    blank=True,
    null=True
)

class SalaryBatch(models.Model):
    batch_name = models.CharField(max_length=100)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.batch_name


class SalaryTransaction(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Success", "Success"),
        ("Failed", "Failed"),
    ]

    batch = models.ForeignKey(
        SalaryBatch,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="transactions"
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="salary_transactions"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    reference = models.CharField(
        max_length=100,
        unique=True,
        default=uuid.uuid4
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.employee.full_name} - {self.amount}"