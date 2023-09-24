from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from .models import Employee, Payslip
from .forms import EmployeeForm, ExcelUploadForm
from .filters import MonthFilter, EmployeeFilter
import pandas as pd
import math
from django.db.models import F


def input_employee_rates(request):
    if request.method == "POST":
        print("Post is done")
        form = EmployeeForm(request.POST)
        if form.is_valid():
            print("form is valid")
            form.save()
            return redirect("success")

    else:
        print("Error")
        form = EmployeeForm()

    return render(request, "services/add_employee.html", {"form": form})


def emlist(request):
    sort_column = request.GET.get("sort", "emp_code")
    employee_filter = EmployeeFilter(request.GET, queryset=Employee.objects.all())

    if sort_column in ["emp_code", "basic"]:
        data = Employee.objects.all()
        data = sorted(data, key=lambda x: int(getattr(x, sort_column)))
    else:
        data = employee_filter.qs.order_by(sort_column)

    context = {
        "data": data,
        "employee_filter": employee_filter,
    }

    return render(request, "services/emlist.html", context)

def delete_employee(request, emp_code):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, emp_code=emp_code)
        employee.delete()
        return redirect('emlist')  # Replace 'employee_list' with the URL name of your employee list page
    else:
        return HttpResponseBadRequest("Invalid Request Method")


def upload_file(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)

        if form.is_valid():
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

            present = {}
            total_days = {}
            for i, j in employee_status.items():
                days_worked = 0
                total_days[i] = len(j)
                for k in j:
                    if k == "P":
                        days_worked += 1
                present[i] = days_worked

            for i, j in employee_total.items():
                ot = 0
                for k in j:
                    hours_worked = k.hour + k.minute / 60
                    diff = hours_worked - 9
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

                selected_month = form.cleaned_data.get("selected_month")

                payslip = Payslip.objects.create(
                    employee=employee,
                    total_days_worked=present[i],
                    absent_days=(total_days[i] - present[i]),
                    overtime_hrs=ot,
                    overtime_rate=ot_amount,
                    total_earnings=total_earnings,
                    gross_salary=gross_salary,
                    total_deductions=total_deductions,
                    net_salary=net_salary,
                    month=selected_month,
                )
                payslip.save()

            return redirect("success")
    else:
        form = ExcelUploadForm()

    return render(request, "services/home.html", {"form": form})


def success(request):
    payslip = MonthFilter(data=request.GET, queryset=Payslip.objects.all())
    return render(request, "services/success.html", {"filter": payslip})


def profile(request, user_id):
    employee = get_object_or_404(Employee, emp_code=user_id)
    payslips = Payslip.objects.filter(employee=employee)
    context = {"employee": employee, "payslips": payslips}
    return render(request, "services/profile.html", context)
