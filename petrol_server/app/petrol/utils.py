# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal
from django.db.models import Sum
from petrol_server.app.petrol import models

def build_discount_transactions(company, start_period='2010-01-01', end_period=None):
    transactions = models.CardTransaction.objects.raw('''
        SELECT
            "petrol_cardtransaction"."id", "petrol_cardtransaction"."made_at", "petrol_cardtransaction"."card_id", "petrol_cardtransaction"."card_holder_id", "petrol_cardtransaction"."petrol_station_id", "petrol_cardtransaction"."fuel", "petrol_cardtransaction"."volume", "petrol_cardtransaction"."price", "petrol_cardtransaction"."is_approved", "petrol_cardtransaction"."is_no_need_attention", SUM(volume * price) AS "amount",
        CASE
            WHEN
                 "petrol_discount"."discount" IS NULL THEN 0 ELSE "petrol_discount"."discount"
            END
        FROM
            "petrol_cardtransaction"
        INNER JOIN
            "petrol_cardholder" ON ( "petrol_cardtransaction"."card_holder_id" = "petrol_cardholder"."id" )
        LEFT JOIN
            "petrol_discount" ON
            ("petrol_cardholder"."company_id" = "petrol_discount"."company_id") AND
            ("petrol_cardtransaction"."made_at" >= "petrol_discount"."date_from") AND
            ("petrol_cardtransaction"."made_at" <= "petrol_discount"."date_to")
        WHERE
            ("petrol_cardholder"."company_id" = %s AND "petrol_cardtransaction"."made_at" BETWEEN '%s' AND '%s')

        GROUP BY
            "petrol_discount"."discount", "petrol_cardtransaction"."id", "petrol_cardtransaction"."made_at", "petrol_cardtransaction"."card_id", "petrol_cardtransaction"."card_holder_id", "petrol_cardtransaction"."petrol_station_id", "petrol_cardtransaction"."fuel", "petrol_cardtransaction"."volume", "petrol_cardtransaction"."price", "petrol_cardtransaction"."is_approved", "petrol_cardtransaction"."is_no_need_attention"
        ''' % (company.id, start_period, end_period))

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
                sum([(card_transaction.discount * card_transaction.volume) for card_transaction in card_transactions]),
                sum([(card_transaction.price - card_transaction.discount)*card_transaction.volume for card_transaction in card_transactions])

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


def get_balance(company, on_date=None):
    transactions = build_discount_transactions(company, end_period=on_date)
    consumption = 0

    t_transactions = models.CardTransaction.objects.filter(
        card_holder__company=company,
        made_at__range = ['2010-01-01', on_date]).annotate(
        amount=Sum('price', field='volume * price')

    ).values_list('amount', flat=True)








    for transaction in transactions:
        consumption += (transaction.price - transaction.discount)*transaction.volume

    payments = models.Payment.objects.filter(
        company_id=company.id,
        date__range=['2011-01-01', on_date]
    ).aggregate(Sum('amount'))['amount__sum']

    if not payments: payments = Decimal(0.00)
    if not consumption: consumption = Decimal(0.00)

    balance = payments - consumption
    return balance
