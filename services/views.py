import pandas as pd
from .forms import ExcelUploadForm
from .models import Employee, Salary
from django.shortcuts import render, redirect


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
                # Set the found header row as column names
                excel_data.columns = header_row

                # Locate the row where the column names are and use it as the header row
                header_row_index = excel_data[
                    excel_data["Emp_Name"] == "Emp_Name"
                ].index[0]

                # Skip the header rows and create Employee objects from the data
                for index, row in excel_data.iloc[header_row_index + 1 :].iterrows():
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

                    salary = Salary.objects.create(
                        Basic=row["Basic"],
                        SA=row["SA"],
                        HRA=row["HRA"],
                        PRA_gain=row["PRA gain"],
                        Overtime=row["OT"],
                        W_F_P=row["W/F(P)"],
                        Bonus=row["Bonus"],
                        LOP=row["LOP"],
                        PRA_loss=row["PRA_loss"],
                        ESI=row["ESI"],
                        ID_Card=row["ID Card"],
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
    return render(request, "services/success.html")
