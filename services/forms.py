
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
        ('january', 'January'), ('february', 'February'), ('march', 'March'), ('april', 'April'),
        ('may', 'May'), ('june', 'June'), ('july', 'July'), ('august', 'August'),
        ('september', 'September'), ('october', 'October'), ('november', 'November'), ('december', 'December'),
    ]

    selected_month = forms.ChoiceField(
        label='Select Month',
        choices=MONTH_CHOICES,
        required=False,  # Allow an empty selection
    )

    year = forms.IntegerField(
        label='Select Year',
        required=False,
    )
