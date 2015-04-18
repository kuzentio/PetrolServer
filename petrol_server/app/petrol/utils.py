import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from petrol_server.app.petrol import models


def company_decorator(user):
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                company = models.Company.objects.get(user__user__id=user.id)
            except ObjectDoesNotExist as e:
                return render_to_response('errors.html', {'error': e})
            return func(company, *args, **kwargs)
        return inner
    return decorator


def staff_required(redirect_url):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_staff:
                return HttpResponseRedirect(redirect_url)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


#@user_passes_test(lambda user: user.is_staff)
#def view(request):
#    pass


def get_balance(company, date=datetime.datetime.now()):
    consumption = models.CardTransaction.objects.filter(
        card_holder__company=company.id,
        made_at__range=['2011-01-01', date]
    ).annotate(
        amount=Sum('id', field='volume * price')
    ).aggregate(
        Sum('amount'))['amount__sum']

    payments = models.Payment.objects.filter(
        company_id=company.id,
        date__range=['2011-01-01', date]
    ).aggregate(Sum('amount'))['amount__sum']
    if not payments: payments = 0
    if not consumption: consumption = 0
    balance = payments - consumption
    return balance


