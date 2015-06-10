from django.test import TestCase
from petrol_server.app.petrol import models
from petrol_server.app.petrol.test import factories
from petrol_server.app.petrol import utils


class TestBalance(TestCase):
    def test_actual_balance(self):
        company = factories.CompanyFactory()
        factories.CardTransactionFactory(volume=10, price=22)
        factories.CardTransactionFactory(volume=10, price=23.80)
        factories.PaymentsFactory(amount=300)

        balance = utils.get_balance(company=company)

        self.assertEqual(len(models.CardTransaction.objects.all()), 2)
        self.assertEqual(balance, -158)


class TestTransactions(TestCase):
    def test_transaction(self):
        company = factories.CompanyFactory()
        card1 = factories.CardFactory(number=u'1')
        card2 = factories.CardFactory(number=u'2')
        cardholder1 = factories.CardHolderFactory(card=card1, company=company)
        cardholder2 = factories.CardHolderFactory(card=card2, company=company)
        period = ['2011-01-01', '2012-01-01']

        transaction1 = factories.CardTransactionFactory(volume=10, price=22, card=card1, card_holder=cardholder1)
        transaction2 = factories.CardTransactionFactory(volume=10, price=23.80, card=card2, card_holder=cardholder2)
        transaction3 = factories.CardTransactionFactory(volume=100, price=23.80, card=card2, card_holder=cardholder2)

        transactions = utils.get_card_transactions(company, start_period=period[0], end_period=period[1])

        self.assertEqual(transactions[0], (card1.number, [transaction1], {'amount': 10.00}, {'total': 220.00}))

