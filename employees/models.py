from django.db import models


class Employee(models.Model):
    employee_id = models.CharField(
        max_length=50,
        unique=True
    )

    full_name = models.CharField(
        max_length=100
    )

    bank_name = models.CharField(
        max_length=100
    )

    account_number = models.CharField(
        max_length=20
    )

    recipient_code = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # Add this field
    bank_code = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name