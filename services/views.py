# views.py
import csv
from attr import validate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .models import Employee, Salary, dept_Choices


def upload_csv(request):
    if request.method == " POST ":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["file"]
            csv_decode = csv_file.read().decode("UTF-8")
            csv_data = csv.reader(csv_decode.splitlines(), delimiter=",")
            next(csv_data)
            updated_csv_data = []

            for row in csv_data:
                department_code = next(
                    (code for code, label in dept_Choices if label == row[2]), "DE"
                )
                employee = Employee.objects.create(
                    Emp_Name=row[0],
                    Emp_Code=row[1],
                    Department=department_code,
                    no_of_days=row[3],
                    days_worked=row[4],
                    Ot_hrs=row[5],
                )
                salary = Salary.objects.create(
                    Basic=row[6],
                    SA=row[7],
                    HRA=row[8],
                    PRA_gain=row[9],
                    Overtime=row[10],
                    W_F_P=row[11],
                    Bonus=row[12],
                    LOP=row[13],
                    PRA_loss=row[14],
                    ESI=row[15],
                    ID_Card=row[16]
                )

                salary.TOTAL_gain = salary.Basic + salary.SA + salary.HRA +salary.PRA_gain
                salary.GROSS_SALARY = salary.TOTAL_gain + salary.Overtime + salary.W_F_P + salary.Bonus
                salary.TOTAL_loss = salary.LOP + salary.PRA_loss + salary.ESI + salary.ID_Card
                salary.NET_SALARY = salary.GROSS_SALARY - salary.TOTAL_loss

                salary.save()

                updated_row = [
                    employee.Emp_Name, employee.Emp_Code, employee.get_Department_display(),
                    employee.no_of_days, employee.days_worked, employee.Ot_hrs,
                    salary.Basic, salary.SA, salary.HRA, salary.PRA_gain, salary.Overtime,
                    salary.W_F_P, salary.Bonus, salary.LOP, salary.PRA_loss, salary.ESI,
                    salary.ID_Card, salary.TOTAL_gain, salary.GROSS_SALARY, salary.TOTAL_loss,
                    salary.NET_SALARY
                ]
                updated_csv_data.append(updated_row)

            # Create a response with the updated CSV data
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="updated_data.csv"'

            # Write the updated CSV data to the response
            writer = csv.writer(response)
            writer.writerow([
                'Emp_Name', 'Emp_Code', 'Department', 'no_of_days', 'days_worked', 'Ot_hrs',
                'Basic', 'SA', 'HRA', 'PRA_gain', 'Overtime', 'W_F_P', 'Bonus', 'LOP',
                'PRA_loss', 'ESI', 'ID_Card', 'TOTAL_gain', 'GROSS_SALARY', 'TOTAL_loss', 'NET_SALARY'
            ])
            writer.writerows(updated_csv_data)

            return redirect("success_page")
    else:
        form = CSVUploadForm()
    return render(request, "upload_csv.html", {"form": form})
