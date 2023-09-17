import pandas as pd
from .forms import ExcelUploadForm
from .models import Employee, Salary
from django.shortcuts import render, redirect
import math  # Import the math module


def home(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_data = pd.read_excel(
                request.FILES["excel_file"], header=None
            )  # Set header to None

            header_row = None
            for index, row in excel_data.iterrows():
                if (
                    "Emp_Name" in row.values
                    and "Emp_Code" in row.values
                    and "Department" in row.values
                ):
                    header_row = row
                    break

            if header_row is not None:
                excel_data.columns = header_row

                # Locate the row where the column names are and use it as the header row
                header_row_index = excel_data[
                    excel_data["Emp_Name"] == "Emp_Name"
                ].index[0]

                # Skip the header rows and create Employee objects from the data
                for index, row in excel_data.iloc[header_row_index + 1 :].iterrows():
                    if not Employee.objects.filter(Emp_Code=row["Emp_Code"]).exists():
                        employee = Employee.objects.create(
                            Emp_Name=row["Emp_Name"],
                            Emp_Code=row["Emp_Code"],
                            Department=row["Department"],
                            no_of_days=row.get(
                                "no_of_days", 0
                            ),  # Handle the possibility of missing columns
                            days_worked=row.get("days_worked", 0),
                            Ot_hrs=None if pd.isna(row["Ot_hrs"]) else int(row["Ot_hrs"]),
                        )
                        employee.save()
                    else:
                        employee = Employee.objects.get(Emp_Code=row["Emp_Code"])
                    salary = Salary.objects.create(
                        emp=employee,
                        Basic=row.get("Basic", 0) if not math.isnan(row["Basic"]) else 0,
                        SA=row.get("SA", 0) if not math.isnan(row["SA"]) else 0,
                        HRA=row.get("HRA", 0) if not math.isnan(row["HRA"]) else 0,
                        PRA_gain=row.get("PRA gain", 0) if not math.isnan(row["PRA gain"]) else 0,
                        Overtime=row.get("OT", 0) if not math.isnan(row["OT"]) else 0,
                        W_F_P=row.get("W/F(P)", 0) if not math.isnan(row["W/F(P)"]) else 0,
                        Bonus=row.get("Bonus", 0) if not math.isnan(row["Bonus"]) else 0,
                        LOP=row.get("LOP", 0) if not math.isnan(row["LOP"]) else 0,
                        PRA_loss=row.get("PRA_loss", 0) if not math.isnan(row["PRA_loss"]) else 0,
                        ESI=row.get("ESI", 0) if not math.isnan(row["ESI"]) else 0,
                        ID_Card=row.get("ID Card", 0) if not math.isnan(row["ID Card"]) else 0,
                    )

                    salary.TOTAL_gain = (
                        salary.Basic + salary.SA + salary.HRA + salary.PRA_gain
                    )
                    salary.GROSS_SALARY = (
                        salary.TOTAL_gain
                        + salary.Overtime
                        + salary.W_F_P
                        + salary.Bonus
                    )
                    salary.TOTAL_loss = (
                        salary.LOP + salary.PRA_loss + salary.ESI + salary.ID_Card
                    )
                    salary.NET_SALARY = salary.GROSS_SALARY - salary.TOTAL_loss
                    salary.save()
                return redirect("success")
            else:
                return render(
                    request,
                    "services/error.html",
                    {"message": "Header row not found in the Excel file"},
                )
    else:
        form = ExcelUploadForm()
    return render(request, "services/home.html", {"form": form})


def success(request):
    salary = Salary.objects.all()
    return render(request, "services/success.html", {"salary":salary})
