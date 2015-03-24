from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from petrol_server.app.petrol import models
from petrol_server.app.petrol.forms import PeriodForm
from petrol_server.app.petrol.utils import staff_required
from datetime import datetime

@login_required(login_url='accounts/login/')
@staff_required(redirect_url='/admin/')
def main(request):
    try:
        company = models.Company.objects.get(user__user__id=request.user.id)
    except ObjectDoesNotExist as e:
        return render_to_response('errors.html', {'error': e})

    if request.method == 'GET':
        form = PeriodForm(request.GET)
        if form.is_valid():
            start_period = datetime.strptime(form['start_period'].value(), '%d.%m.%Y')
            end_period = datetime.strptime(form['end_period'].value(), '%d.%m.%Y')

            transactions = models.CardTransaction.objects.filter(
                card__company__id=company.id).filter(
                made_at__range=[start_period, end_period]
            )
            cont = {'transactions': transactions,
                    'form': PeriodForm,
                    'company': company, }

            return render_to_response('card_transactions.html', cont)
    cont = {'form': PeriodForm, 'company': company}
    return render_to_response('card_transactions.html', cont)


@login_required(login_url='accounts/login/')
def logout_view(request):
    logout(request)
    return render_to_response('success_logout.html')









