from django import forms
from .models import Footage
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput


class FilterForm(forms.ModelForm):

    start_time = forms.TimeField(widget=TimePickerInput(), initial='10:00')
    end_time = forms.TimeField(widget=TimePickerInput(), initial='18:00')
    date = forms.DateField(widget=DatePickerInput(format='%d.%m.%Y'))

    class Meta:
        model = Footage
        fields = ('footype', 'foocause')
