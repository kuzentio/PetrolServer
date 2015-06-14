from django import forms

import datetime

class PeriodForm(forms.Form):
    start_period = forms.DateField(input_formats=['%d.%m.%Y'], initial=datetime.datetime.today().strftime("%d.%m.%Y"))
    end_period = forms.DateField(input_formats=['%d.%m.%Y'], initial=(datetime.datetime.today()
                                                                      - datetime.timedelta(30/1)).strftime("%d.%m.%Y"))
