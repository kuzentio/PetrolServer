from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from petrol_server.app.petrol import models


def render_decorator(template):
    def decorator(func):
        def inner(*args, **kwargs):
            context = func(*args, **kwargs)
            return render_to_response(template, context)
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


def get_balance(company):
    consumption = models.CardTransaction.objects.filter(
        card_holder__company=company.id
    ).annotate(
        amount=Sum('id', field='volume * price')
    ).aggregate(
        Sum('amount'))['amount__sum']

    payments = models.Payment.objects.filter(
        company_id=company.id
    ).aggregate(Sum('amount'))['amount__sum']
    if not payments: payments = 0
    if not consumption: consumption = 0
    balance = payments - consumption
    return balance


