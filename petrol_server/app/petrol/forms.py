from django import forms


class PeriodForm(forms.Form):
    start_period = forms.DateField(input_formats=['%d.%m.%Y'])
    end_period = forms.DateField(input_formats=['%d.%m.%Y'])