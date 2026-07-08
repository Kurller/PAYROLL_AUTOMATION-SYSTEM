import uuid
import pandas as pd
from io import StringIO

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from employees.models import Employee
from .models import SalaryBatch, SalaryTransaction
from .serializers import PayrollUploadSerializer


class SalaryTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryTransaction
        fields = "__all__"


class SalaryTransactionListView(ListAPIView):
    queryset = SalaryTransaction.objects.all()
    serializer_class = SalaryTransactionSerializer


class PayrollUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="Upload a payroll CSV or Excel file.",
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                description="CSV or Excel (.csv, .xlsx) payroll file",
                type=openapi.TYPE_FILE,
                required=True,
            )
        ],
        consumes=["multipart/form-data"],
    )
    def post(self, request):

        serializer = PayrollUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        uploaded_file = request.FILES["file"]

        extension = uploaded_file.name.split(".")[-1].lower()

        try:

            uploaded_file.seek(0)
            file_header = uploaded_file.read(4)
            uploaded_file.seek(0)

            if file_header.startswith(b"PK"):

                df = pd.read_excel(
                    uploaded_file,
                    dtype={
                        "employee_id": str,
                        "bank_code": str,
                        "account_number": str,
                    },
                )

            elif extension == "csv":

                content = uploaded_file.read()

                try:
                    decoded_content = content.decode("utf-8-sig")
                except UnicodeDecodeError:
                    decoded_content = content.decode("latin-1")

                df = pd.read_csv(
                    StringIO(decoded_content),
                    dtype=str,
                )

            else:

                return Response(
                    {
                        "status": False,
                        "error": "Only CSV, XLSX and XLS files are supported",
                    },
                    status=400,
                )

            df.columns = (
                df.columns
                .str.replace("\ufeff", "", regex=False)
                .str.strip()
                .str.lower()
            )

            required_columns = [
                "employee_id",
                "full_name",
                "bank_name",
                "bank_code",
                "account_number",
                "amount",
            ]

            missing = [
                col for col in required_columns
                if col not in df.columns
            ]

            if missing:
                return Response(
                    {
                        "status": False,
                        "error": f"Missing columns: {missing}",
                    },
                    status=400,
                )

            errors = []

            for index, row in df.iterrows():

                if pd.isna(row["employee_id"]):
                    errors.append(f"Row {index+1}: Employee ID missing")

                if pd.isna(row["account_number"]):
                    errors.append(f"Row {index+1}: Account number missing")

                if pd.isna(row["amount"]):
                    errors.append(f"Row {index+1}: Amount missing")

                elif float(row["amount"]) <= 0:
                    errors.append(f"Row {index+1}: Invalid amount")

            if errors:
                return Response(
                    {
                        "status": False,
                        "validation_errors": errors,
                    },
                    status=400,
                )

            batch = SalaryBatch.objects.create(
                batch_name=uploaded_file.name
            )

            created_count = 0

            for _, row in df.iterrows():

                employee, created = Employee.objects.get_or_create(
                    employee_id=str(row["employee_id"]),
                    defaults={
                        "full_name": str(row["full_name"]),
                        "bank_name": str(row["bank_name"]),
                        "bank_code": str(row["bank_code"]),
                        "account_number": str(row["account_number"]),
                    },
                )

                if not created:
                    employee.full_name = str(row["full_name"])
                    employee.bank_name = str(row["bank_name"])
                    employee.bank_code = str(row["bank_code"])
                    employee.account_number = str(row["account_number"])
                    employee.save()

                SalaryTransaction.objects.create(
                    employee=employee,
                    batch=batch,
                    amount=float(row["amount"]),
                    reference=str(uuid.uuid4()),
                )

                created_count += 1

            return Response(
                {
                    "status": True,
                    "message": "Payroll uploaded successfully",
                    "batch_id": batch.id,
                    "transactions_created": created_count,
                }
            )

        except Exception as e:
            return Response(
                {
                    "status": False,
                    "error": str(e),
                },
                status=500,
            )