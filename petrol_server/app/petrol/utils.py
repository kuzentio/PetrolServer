# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal
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
def get_transactions(company, start_period=None, end_period=None):

    return models.CardTransaction.objects.filter(
                card_holder__company=company.id).filter(
                made_at__range=[start_period, end_period]
            ).annotate(
                amount=Sum('price', field='volume * price')
            ).order_by('made_at')


def get_card_transactions(company, start_period=None, end_period=None):
    transactions_data = []

    transactions = models.CardTransaction.objects.filter(
                card_holder__company=company.id).filter(
                made_at__range=[start_period, end_period]
            ).annotate(
                amount=Sum('price', field='volume * price')
            ).order_by('made_at')
    discounts = models.Discount.objects.filter(company=company)

    seen = set()
    cards = [transaction.card for transaction in transactions if transaction.card not in seen and not seen.add(transaction.card)]

    for card in cards:
        amount_litres = transactions.filter(card=card).aggregate(amount=Sum('volume', field='volume'))
        amount_money = transactions.filter(card=card).aggregate(total=Sum('amount'))
        card_transactions = [transaction for transaction in transactions if transaction.card == card]

        for card_transaction in card_transactions:
            for discount in discounts:
                if (card_transaction.made_at >= discount.date_from) and (card_transaction.made_at <= discount.date_to):
                    card_transaction.discount = discount.discount
                    card_transaction.discount_price = card_transaction.price - discount.discount
                else:
                    card_transaction.discount = 0.00
                    card_transaction.discount_price = card_transaction.price
            card_transaction.amount_discount_money = card_transaction.volume * card_transaction.discount_price

        transactions_data.append(
            (
                (card.number, ) + (
                    card_transactions,
                ) + (
                    amount_litres,
                ) + (
                    amount_money,
                )
            )
        )

    return transactions_data


def get_balance(company, on_date=datetime.datetime.now()):
    consumption = get_transactions(
        company,
        start_period='2011-01-01',
        end_period=on_date).aggregate(Sum('amount'))['amount__sum']

    payments = models.Payment.objects.filter(
        company_id=company.id,
        date__range=['2011-01-01', on_date]
    ).aggregate(Sum('amount'))['amount__sum']

    if not payments: payments = Decimal(0.00)
    if not consumption: consumption = Decimal(0.00)

    balance = payments - consumption
    return balance


