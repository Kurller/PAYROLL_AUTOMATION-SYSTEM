from django.urls import path
from .views import (
    PayrollUploadView,
    SalaryTransactionListView
)

urlpatterns = [
    path(
        'upload/',
        PayrollUploadView.as_view()
    ),

    path(
        'transactions/',
        SalaryTransactionListView.as_view()
    )
]