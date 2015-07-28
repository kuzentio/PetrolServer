from decimal import Decimal
from django.test import TestCase
from petrol_server.app.petrol import models
from petrol_server.app.petrol.test import factories
from petrol_server.app.petrol import utils


class TestBalance(TestCase):
    def test_balance(self):
        company = factories.CompanyFactory()
        factories.CardTransactionFactory(volume=10, price=22)
        factories.CardTransactionFactory(made_at='2012-01-01', volume=10, price=23.80)
        factories.DiscountFactory(discount=0.22)
        factories.PaymentsFactory(amount=300)

        balance = utils.get_balance(company=company)

        self.assertEqual(float(balance), -155.80)

    def test_balance_for_transactions_with_payment(self):
        company = factories.CompanyFactory()
        factories.CardTransactionFactory(volume=10, price=22)
        factories.CardTransactionFactory(made_at='2012-01-01', volume=10, price=23.80)

        balance = utils.get_balance(company=company)

        self.assertEqual(float(balance), -458)

    def test_balance_for_transactions(self):
        company = factories.CompanyFactory()
        factories.CardTransactionFactory(volume=10, price=22)
        factories.CardTransactionFactory(made_at='2012-01-01', volume=10, price=23.80)

        balance = utils.get_balance(company=company)

        self.assertEqual(float(balance), -458)


class TestTransactions(TestCase):
    def setUp(self):
        self.company_foo = factories.CompanyFactory(title='Foo')
        self.company_bar = factories.CompanyFactory(title='Bar')
        self.card_01 = factories.CardFactory(number='001')
        self.card_02 = factories.CardFactory(number='002')
        self.cardholder_01 = factories.CardHolderFactory(company=self.company_foo, card=self.card_01)
        self.cardholder_02 = factories.CardHolderFactory(company=self.company_bar, card=self.card_02)
        factories.CardTransactionFactory(card=self.card_01, card_holder=self.cardholder_01)
        factories.CardTransactionFactory(card=self.card_02, card_holder=self.cardholder_02, volume=11, price=20, made_at='2011-01-02')
        factories.CardTransactionFactory(card=self.card_02, card_holder=self.cardholder_02, volume=15, price=22, made_at='2011-01-02')
        factories.CardTransactionFactory(card=self.card_02, card_holder=self.cardholder_02, volume=19.99, price=22, made_at='2011-01-03')
        factories.DiscountFactory(company=self.company_bar, discount=0.30, date_from='2011-01-01', date_to='2011-01-02')
        factories.DiscountFactory(company=self.company_foo, discount=0.15, date_from='2011-01-01', date_to='2011-01-02')

    def test_balance(self):
        balance = utils.get_balance(company=self.company_bar, on_date='2011-01-02')

        self.assertFalse(1, False)

