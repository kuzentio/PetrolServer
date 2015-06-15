from django import forms
from petrol_server.app.petrol import models

import datetime


class PeriodForm(forms.Form):
    start_period = forms.DateField(input_formats=['%d.%m.%Y'],
                                   initial=datetime.datetime.today().strftime("%d.%m.%Y")
                                   )
    end_period = forms.DateField(input_formats=['%d.%m.%Y'],
                                 initial=(datetime.datetime.today()
                                 - datetime.timedelta(30/1)).strftime("%d.%m.%Y")
                                 )


class DiscountForm(forms.Form):

    class Meta:
        model = models.Discount
