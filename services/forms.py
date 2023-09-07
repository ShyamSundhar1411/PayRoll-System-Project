from django import forms
from .models import Employee, Salary

class CSVUploadForm(forms.ModelForm):
    class Meta:
        model = Employee, Salary
        fields = '__all__'