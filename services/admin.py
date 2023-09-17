from django.contrib import admin
from .models import Employee,Payslip
# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_name', 'emp_code', 'basic_pay', 'sa')
    search_fields = ('emp_name', 'emp_code')

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ('employee','total_days_worked','overtime_hrs','overtime_rate','gross_salary')