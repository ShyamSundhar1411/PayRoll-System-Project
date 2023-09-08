import pandas as pd
from .forms import ExcelUploadForm
from .models import Employee
from django.shortcuts import render, redirect

def home(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_data = pd.read_excel(request.FILES['excel_file'])
            for index, row in excel_data.iterrows():
                Employee.objects.create(
                    Emp_Name=row['Emp_Name'],
                    Emp_Code=row['Emp_Code'],
                    Department=row['Department'],
                    no_of_days=row['no_of_days'],
                    days_worked=row['days_worked'],
                    Ot_hrs=row['Ot_hrs']
                )
            return redirect('success')
    else:
        form = ExcelUploadForm()
    return render(request, 'services/home.html', {'form': form})

def success(request):
    return render(request, 'services/success.html')

