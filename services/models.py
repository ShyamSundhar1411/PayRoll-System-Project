from django.db import models

dept_Choices = [("AA","Accounts&Admin"),("AS","Assembly"),("CT","Controls"),("CO","Cooking"),("DE","Default"),("DS","Designing"),("EL","Electrical"),("HK","House Keeping"),("MA","Manufacturing"),("PU","Purchase")]

class Employee(models.Model):
    Emp_Name = models.CharField(max_length=100)
    Emp_Code = models.PositiveSmallIntegerField(primary_key=True)
    Department = models.CharField(max_length=100, choices=dept_Choices, default="DE")
    no_of_days = models.PositiveSmallIntegerField()
    days_worked = models.PositiveSmallIntegerField()
    Ot_hrs = models.PositiveSmallIntegerField()
