from bootstrap_datepicker_plus import DatePickerInput
from django import forms

class ToDoForm(forms.Form):
    todo = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
    date = forms.DateField(widget=DatePickerInput(format= "mm/dd/yyyy"))