import pandas as pd
from .forms import ExcelUploadForm
from .models import Employee
from django.shortcuts import render, redirect

def home(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_data = pd.read_excel(request.FILES['excel_file'], header=None) 

            header_row = None
            for index, row in excel_data.iterrows():
                if 'Emp_Name' in row.values and 'Emp_Code' in row.values and 'Department' in row.values:
                    header_row = row
                    break

            if header_row is not None:
                excel_data.columns = header_row
                header_row_index = excel_data[excel_data['Emp_Name'] == 'Emp_Name'].index[0]
                for index, row in excel_data.iloc[header_row_index + 1:].iterrows():
                    Employee.objects.create(
                        Emp_Name=row['Emp_Name'],
                        Emp_Code=row['Emp_Code'],
                        Department=row['Department'],
                        no_of_days=row.get('no_of_days', 0),  # Handle the possibility of missing columns
                        days_worked=row.get('days_worked', 0),
                        Ot_hrs=None if pd.isna(row['Ot_hrs']) else int(row['Ot_hrs'])
                    )
                return redirect('success')
            else:
                return render(request, 'services/error.html', {'message': 'Header row not found in the Excel file'})
    else:
        form = ExcelUploadForm()
    return render(request, 'services/home.html', {'form': form})

def success(request):
    return render(request, 'services/success.html')
