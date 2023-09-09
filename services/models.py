from django.db import models

dept_Choices = [("AA","Accounts&Admin"),("AS","Assembly"),("CT","Controls"),("CO","Cooking"),("DE","Default"),("DS","Designing"),("EL","Electrical"),("HK","House Keeping"),("MA","Manufacturing"),("PU","Purchase")]

class Employee(models.Model):
    Emp_Name = models.CharField(max_length=100)
    Emp_Code = models.PositiveSmallIntegerField(primary_key=True)
    Department = models.CharField(max_length=100, choices=dept_Choices, default="DE")
    no_of_days = models.PositiveSmallIntegerField()
    days_worked = models.PositiveSmallIntegerField()
    Ot_hrs = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return self.Emp_Name

class Salary(models.Model):
    emp  = models.ForeignKey('Employee', on_delete=models.CASCADE,)

    # earnings
    Basic = models.DecimalField(max_digits=10,decimal_places=2)
    SA = models.DecimalField(max_digits=10,decimal_places=2)
    HRA = models.DecimalField(max_digits=10,decimal_places=2)
    PRA_gain = models.DecimalField(max_digits=10,decimal_places=2)
    Overtime = models.DecimalField(max_digits=10,decimal_places=2)
    W_F_P = models.DecimalField(max_digits=10,decimal_places=2)
    Bonus = models.DecimalField(max_digits=10,decimal_places=2)

    # deductions
    LOP = models.DecimalField(max_digits=10,decimal_places=2)
    PRA_loss = models.DecimalField(max_digits=10,decimal_places=2)
    ESI = models.DecimalField(max_digits=10,decimal_places=2)
    ID_Card =models.DecimalField(max_digits=10,decimal_places=2)

    #salary
    TOTAL_gain = models.DecimalField(max_digits=10,decimal_places=2)
    GROSS_SALARY = models.DecimalField(max_digits=10,decimal_places=2)
    TOTAL_loss = models.DecimalField(max_digits=10,decimal_places=2)
    NET_SALARY = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.emp.Emp_Name