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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add a CSS class to each input field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'custom-input'

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        label="Upload Excel File",
        help_text="Upload the Excel file containing employee data.",
    )

    month = forms.CharField(
        label="Month",
        max_length=255,  # Adjust the max length as needed
        help_text="Enter the month for the data (e.g., January 2023).",
    )
