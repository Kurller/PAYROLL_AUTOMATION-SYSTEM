from django.urls import path

from .views import (
    TestPaystackView,
    CreateRecipientView,
    ProcessPaymentView,
    ProcessAllPaymentsView
)

urlpatterns = [

    path(
        "test/",
        TestPaystackView.as_view()
    ),

    path(
        "recipient/<int:employee_id>/",
        CreateRecipientView.as_view()
    ),

    path(
        "process/<int:transaction_id>/",
        ProcessPaymentView.as_view()
    ),

    path(
        "process-all/",
        ProcessAllPaymentsView.as_view()
    ),
]