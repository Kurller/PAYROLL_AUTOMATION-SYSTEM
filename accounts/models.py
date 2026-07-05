from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("hr", "HR"),
        ("finance", "Finance")
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="hr"
    )
class SalaryBatch(models.Model):

    STATUS_CHOICES = [

        ("Pending","Pending"),
        ("Approved","Approved"),
        ("Processed","Processed")
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    def __str__(self):

        return (
            f"{self.user.username} - "
            f"{self.role}"
        )