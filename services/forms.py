
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
        ('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'),
        ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'),
        ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December'),
    ]

    selected_month = forms.ChoiceField(
        label='Select Month',
        choices=MONTH_CHOICES,
        required=False,  # Allow an empty selection
    )
