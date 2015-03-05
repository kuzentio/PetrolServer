
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http import HttpResponse
from petrol_server.app.petrol import models
from petrol_server.app.petrol.forms import PeriodForm
from petrol_server.app.petrol.utils import render_decorator
from datetime import datetime

@login_required(login_url='accounts/login/')
@render_decorator(template='card_transactions.html')
def main(request):
    if request.method == 'GET':
        form = PeriodForm(request.GET)
        if form.is_valid():
            start_period = datetime.strptime(form['start_period'].value(), '%d.%m.%Y')
            end_period = datetime.strptime(form['end_period'].value(), '%d.%m.%Y')
            comp = models.Company.objects.filter(users__user__id=request.user.id)

            transactions = models.CardTransaction.objects.filter(card__company__id=comp[0].id).filter(
                                                                 made_at__range=[start_period, end_period])

            cont = {'transactions': transactions, 'form': PeriodForm }
            cont.update(csrf(request))
            return cont
    cont = {'form': PeriodForm}
    return cont









