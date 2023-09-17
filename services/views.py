import pandas as pd
from django.shortcuts import render, redirect
from .models import Employee, Payslip
from .forms import EmployeeForm, ExcelUploadForm
import math


def input_employee_rates(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("success")

    else:
        form = EmployeeForm()

    return render(request, "services/add_employee.html", {"form": form})


def upload_file(request):
    if request.method == "POST":
        excel_form = ExcelUploadForm(request.POST, request.FILES)

        if excel_form.is_valid():
            excel_file = request.FILES["excel_file"]
            df = pd.read_excel(excel_file)

            employee_status = {}
            employee_total = {}
            current_emp_code = None
            for index, row in df.iterrows():
                emp_code = row["Emp_Code"]
                status = row["Status"]
                total = row["Total"]
                if not pd.isna(emp_code):
                    current_emp_code = emp_code
                    employee_status[current_emp_code] = []
                    employee_total[current_emp_code] = []
                if not pd.isna(status):
                    employee_status[current_emp_code].append(status)
                    employee_total[current_emp_code].append(total)

            for i, j in employee_status.items():
                days_worked = 0
                total_days = len(j)
                for k in j:
                    if k == "P":
                        days_worked += 1

            for i, j in employee_total.items():
                ot = 0
                for k in j:
                    hours_worked = k.hour + k.minute / 60
                    diff = hours_worked - 9
                    print(diff)
                    ot += max(math.floor(diff), 0)
                employee = Employee.objects.get(emp_code=i)
                basicpay_perday = employee.basic_pay / 30
                basicpay_perhour = basicpay_perday / 24
                ot_amount = basicpay_perhour * ot

                total_earnings = (
                    employee.basic_pay + employee.sa + employee.hra + employee.pra_gain
                )

                gross_salary = total_earnings + employee.att_bonus + ot_amount

                total_deductions = (
                    employee.pra_loss + employee.esi + employee.lop + employee.id_card
                )

                net_salary = gross_salary - total_deductions

                payslip = Payslip.objects.create(
                    employee=employee,
                    total_days_worked=days_worked,
                    absent_days=(total_days - days_worked),
                    overtime_hrs=ot,
                    overtime_rate=ot_amount,
                    total_earnings=total_earnings,
                    gross_salary=gross_salary,
                    total_deductions=total_deductions,
                    net_salary=net_salary,
                )
                payslip.save()

            return redirect("success")
    else:
        excel_form = ExcelUploadForm()

    return render(request, "services/home.html", {"excel_form": excel_form})


def success(request):
    return render(request, "services/success.html")
