from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.shortcuts import render_to_response
from petrol_server.app.petrol import models
from petrol_server.app.petrol import forms
from petrol_server.app.petrol import utils
from datetime import datetime


@login_required(login_url='accounts/login/')
@user_passes_test(lambda user: not user.is_staff, login_url='/admin/')
def main(request):
    try:
        company = models.Company.objects.get(user__user=request.user.id)
    except ObjectDoesNotExist as e:
        return render_to_response('errors.html', {'error': e})

    form = forms.PeriodForm(request.GET)
    balance = utils.get_balance(company, on_date=datetime.now())
    context = {
        'form': forms.PeriodForm,
        'company': company,
        'balance': balance,
        }
    if form.is_valid():
        start_period = datetime.strptime(form['start_period'].value(), '%d.%m.%Y')
        end_period = datetime.strptime(form['end_period'].value(), '%d.%m.%Y')
        transactions = utils.build_discount_transactions(company, start_period, end_period)
        context = {
                'summary_data': utils.get_summary_data(transactions),
                'card_transactions': utils.get_card_transactions(transactions),
                'form': form,
                'company': company,
                'balance': balance,
                }

    return render_to_response('card_transactions.html', context)

@login_required(login_url='accounts/login/')
@user_passes_test(lambda user: user.is_staff, login_url='/admin/')
def statistic(request):
    form = forms.PeriodForm(request.GET)

    if not form.is_valid():
        return render_to_response('statistic.html', {'form': form})

    start_period = datetime.strptime(form['start_period'].value(), '%d.%m.%Y')
    end_period = datetime.strptime(form['end_period'].value(), '%d.%m.%Y')

    companies_data = models.CardTransaction.objects.filter(
        made_at__range=[start_period, end_period],
    ).values_list(
        'card_holder__company__title',
    ).annotate(
        amount=Sum('price', field='volume * price'),
        volume=Sum('volume'),
    )

    companies_data = [(utils.get_balance(models.Company.objects.get(title=company_data[0]), start_period), utils.get_balance(models.Company.objects.get(title=company_data[0]), end_period),) + company_data for company_data in companies_data]

    context = {
        'form': form,
        'companies_data': companies_data,
    }

    return render_to_response('statistic.html', context)


@login_required(login_url='accounts/login/')
@user_passes_test(lambda user: not user.is_staff, login_url='/admin/')
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

