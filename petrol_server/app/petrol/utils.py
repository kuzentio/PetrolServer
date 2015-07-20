# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal
from django.db.models import Sum, Q
from petrol_server.app.petrol import models


class Statistic_obj(object):
    def __init__(self, company, realization, amount, amount_discount):
        self.company = company.title
        self.realizations = realization
        self.amount = amount
        self.amount_discount = amount_discount

    def __repr__(self):
        return self.company

def build_discount_transactions(company, start_period='2010-01-01', end_period=None):
    transactions = models.CardTransaction.objects.select_related().filter(
                card_holder__company=company.id).filter(
                made_at__range=[start_period, end_period]
            ).annotate(
                amount=Sum('price', field='volume * price')
            ).order_by('made_at')

    discounts = models.Discount.objects.select_related().filter(company=company).filter(
                Q(date_from__range=[start_period, end_period]) |
                Q(date_to__range=[start_period, end_period])
    )

    if discounts:
        for transaction in transactions:
            for discount in discounts:
                if transaction.made_at >= discount.date_from and transaction.made_at <= discount.date_to:
                    transaction.discount = discount.discount
                    transaction.discount_price = transaction.price - transaction.discount
                    transaction.amount_discount_money = transaction.volume * transaction.discount_price
                else:
                    transaction.discount = Decimal(0.00)
                    transaction.discount_price = Decimal(0.00)
                    transaction.amount_discount_money = transaction.amount
    else:
        for transaction in transactions:
            transaction.discount = Decimal(0.00)
            transaction.discount_price = Decimal(0.00)
            transaction.amount_discount_money = transaction.amount

    return transactions


def get_card_transactions(transactions):
    card_transactions_data = []

    cards = set([transaction.card for transaction in transactions])
    for card in cards:
        card_transactions = [transaction for transaction in transactions if card == transaction.card]
        card_transactions_data.append(
            (
                card, card_transactions,
                sum([card_transaction.volume for card_transaction in card_transactions]),
                sum([card_transaction.amount for card_transaction in card_transactions]),
                sum([card_transaction.amount_discount_money for card_transaction in card_transactions])
            )
        )
    return card_transactions_data


def get_summary_data(transactions):
    summary_data = {}
    summary_data['fuel'] = {}
    total = 0
    saved_money = 0

    for card_transaction in transactions:
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
    transactions = build_discount_transactions(company, end_period=on_date)
    consumption = 0

    for transaction in transactions:
        consumption += transaction.amount_discount_money


    payments = models.Payment.objects.filter(
        company_id=company.id,
        date__range=['2011-01-01', on_date]
    ).aggregate(Sum('amount'))['amount__sum']

    if not payments: payments = Decimal(0.00)
    if not consumption: consumption = Decimal(0.00)

    balance = payments - consumption
    return balance
