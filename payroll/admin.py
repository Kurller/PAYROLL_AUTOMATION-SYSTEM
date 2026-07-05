from django.contrib import admin


from .models import SalaryBatch, SalaryTransaction

admin.site.register(SalaryBatch)
admin.site.register(SalaryTransaction)