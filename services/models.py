from datetime import date
from django.db import models


class Employee(models.Model):
    emp_code = models.IntegerField(primary_key=True)
    emp_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    dob = models.DateField()
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    sa = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    pra_gain = models.DecimalField(max_digits=10, decimal_places=2)
    att_bonus = models.DecimalField(max_digits=10, decimal_places=2)
    pra_loss = models.DecimalField(max_digits=10, decimal_places=2)
    esi = models.DecimalField(max_digits=10, decimal_places=2)
    lop = models.DecimalField(max_digits=10, decimal_places=2)
    id_card = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.emp_name


class Payslip(models.Model):
    employee = models.ForeignKey(
        Employee, to_field="emp_code", on_delete=models.CASCADE
    )
    month = models.CharField(max_length=15)
    year = models.IntegerField(default=date.today().year)
    total_days_worked = models.IntegerField()
    absent_days = models.IntegerField()
    overtime_hrs = models.DecimalField(max_digits=10, decimal_places=2)
    overtime_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.employee.emp_name