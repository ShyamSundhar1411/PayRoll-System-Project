from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "emp_code",
            "emp_name",
            "basic_pay",
            "sa",
            "hra",
            "pra_gain",
            "att_bonus",
            "pra_loss",
            "esi",
            "lop",
            "id_card",
        ]


class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        label="Upload Excel File",
        help_text="Upload the Excel file containing employee data.",
    )
