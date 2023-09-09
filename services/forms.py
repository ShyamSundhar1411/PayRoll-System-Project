from django import forms

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label="Salary Summary",help_text="Upload the Salary Summary in the form of .csv")
