# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from petrol_server.app.petrol import models


def staff_required(redirect_url):
    # TODO: check user_passes_test
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_staff:
                return HttpResponseRedirect(redirect_url)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def filter_transactions(company, start_period='2010-01-01', end_period=None):
    return models.CardTransaction.objects.filter(
                card_holder__company=company.id).filter(
                made_at__range=[start_period, end_period]
            ).annotate(
                amount=Sum('price', field='volume * price')
            ).order_by('made_at')


def get_card_transactions(transactions):
    transactions_data = []

    cards = set([transaction.card for transaction in transactions])

    for card in cards:
        amount_litres = transactions.filter(card=card).aggregate(amount=Sum('volume', field='volume'))
        amount_money = transactions.filter(card=card).aggregate(total=Sum('amount'))
        card_transactions = get_discount_transactions(
            [transaction for transaction in transactions if transaction.card == card]
        )
        for card_transaction in card_transactions:
            card_transaction.discount_price = card_transaction.price - card_transaction.discount
            card_transaction.amount_discount_money = card_transaction.volume * card_transaction.discount_price

        transactions_data.append(
            (
                card.number, card_transactions, amount_litres, amount_money
            )
        )
    return transactions_data


def get_summary_data(transactions):
    summary_data = {}
    summary_data['fuel'] = {}
    total = 0
    saved_money = 0

    card_transactions = get_discount_transactions(transactions)

    for card_transaction in card_transactions:
        total += card_transaction.amount
        saved_money += card_transaction.discount * card_transaction.volume
        try:
            summary_data['fuel'][card_transaction.fuel] += card_transaction.volume
        except KeyError:
            summary_data['fuel'][card_transaction.fuel] = card_transaction.volume

    summary_data['total'] = total
    summary_data['saved_money'] = saved_money

    return summary_data


def get_balance(company, on_date=datetime.datetime.now()):
    transactions = filter_transactions(company, end_period=on_date)
    transactions = get_discount_transactions(transactions)
    consumption = 0

    for transaction in transactions:
        transaction.discount_price = transaction.price - transaction.discount
        transaction.amount_discount_money = transaction.volume * transaction.discount_price
        consumption += transaction.amount_discount_money

    payments = models.Payment.objects.filter(
        company_id=company.id,
        date__range=['2011-01-01', on_date]
    ).aggregate(Sum('amount'))['amount__sum']

    if not payments: payments = Decimal(0.00)
    if not consumption: consumption = Decimal(0.00)

    balance = payments - consumption
    return balance


def get_discount_transactions(transactions):

    for transaction in transactions:
        discounts = models.Discount.objects.filter(company=transaction.card_holder.company)
        if not discounts:
            transaction.discount = Decimal(0.00)
        for discount in discounts:
            if transaction.made_at >= discount.date_from and transaction.made_at <= discount.date_to:
                transaction.discount = discount.discount
            else:
                transaction.discount = Decimal(0.00)

    return transactions

