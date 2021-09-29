from django.forms import ModelForm
from django import forms

## Add import from CSV button
class UploadFileForm(forms.Form):
    csv_file = forms.FileField()