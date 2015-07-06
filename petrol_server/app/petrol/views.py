from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from petrol_server.app.petrol import models
from petrol_server.app.petrol import forms
from petrol_server.app.petrol import utils
from datetime import datetime
from petrol_server.app.petrol.utils import staff_required


@login_required(login_url='accounts/login/')
@staff_required(redirect_url='/admin/')
def main(request):
    try:
        company = models.Company.objects.get(user__user__id=request.user.id)
    except ObjectDoesNotExist as e:
        return render_to_response('errors.html', {'error': e})
    balance = utils.get_balance(company)

    if request.method == 'GET':
        form = forms.PeriodForm(request.GET)
        if form.is_valid():
            start_period = datetime.strptime(form['start_period'].value(), '%d.%m.%Y')
            end_period = datetime.strptime(form['end_period'].value(), '%d.%m.%Y')
            card_transactions = utils.get_card_transactions(company, start_period, end_period)
            context = {
                    'card_transactions': card_transactions,
                    'form': form,
                    'company': company,
                    'balance': balance,
                    }

            return render_to_response('card_transactions.html', context)
    context = {
        'form': forms.PeriodForm,
        'company': company,
        'balance': balance
        }
    return render_to_response('card_transactions.html', context)


@login_required(login_url='accounts/login/')
@staff_required(redirect_url='/admin/')
def balance(request, company_id):
    try:
        company = models.Company.objects.get(user__user__id=request.user.id)
    except ObjectDoesNotExist as e:
        return render_to_response('errors.html', {'error': e})

    payments = models.Payment.objects.filter(
        company_id=company_id
    ).order_by('date')
    for payment in payments:
        payment.balance = utils.get_balance(company, payment.date)

    context = {'payments': payments}

    return render_to_response('payments.html', context)


def logout_view(request):
    logout(request)
    return render_to_response('success_logout.html')

