
from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

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

    MONTH_CHOICES = [
        ('', 'Select Month'),
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'),
    ]

    selected_month = forms.ChoiceField(
        label='Select Month',
        choices=MONTH_CHOICES,
        required=False,  # Allow an empty selection
    )
