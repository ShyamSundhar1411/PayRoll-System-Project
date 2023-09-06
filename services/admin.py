from django.contrib import admin
from .models import Employee,Salary
# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('Emp_Name', 'Emp_Code', 'Department')
    search_fields = ('Emp_Name', 'Emp_Code')

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('id','emp','Basic','LOP','GROSS_SALARY', 'TOTAL_loss', 'NET_SALARY')