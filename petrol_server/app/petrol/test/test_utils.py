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
    def test_transactions(self):
        company = factories.CompanyFactory()
        card1 = factories.CardFactory(number=u'1')
        card2 = factories.CardFactory(number=u'2')
        cardholder1 = factories.CardHolderFactory(card=card1, company=company)
        cardholder2 = factories.CardHolderFactory(card=card2, company=company)
        period = ['2011-01-01', '2012-01-01']

        transaction1 = factories.CardTransactionFactory(volume=10, price=22, card=card1, card_holder=cardholder1)
        transaction2 = factories.CardTransactionFactory(volume=10, price=23.80, card=card2, card_holder=cardholder2)
        transaction3 = factories.CardTransactionFactory(volume=100, price=23.80, card=card2, card_holder=cardholder2)
        transactions = utils.filter_transactions(company, start_period=period[0], end_period=period[1])

        card_transactions = utils.get_card_transactions(transactions)

        number, trans, amount, total = card_transactions[0]

        self.assertEqual(number, card1.number)
        self.assertEqual(trans[0], transaction1)
        self.assertEqual(amount, {'amount': 10.00})
        self.assertEqual(total, {'total': 220.00})

        number, trans, amount, total = card_transactions[1]

        self.assertEqual(number, card2.number)
        self.assertEqual(trans[0], transaction2)
        self.assertEqual(trans[1], transaction3)
        self.assertEqual(amount, {'amount': 110.00})
        self.assertEqual(total, {'total': 238+2380})

    def test_discount_transactions(self):

        company = factories.CompanyFactory()
        period = ['2010-01-01', '2012-01-01']

        factories.CardTransactionFactory(volume=10, price=22, made_at='2011-01-01')
        factories.CardTransactionFactory(volume=10, price=23.80, made_at='2011-01-02')
        factories.CardTransactionFactory(volume=100, price=23.80, made_at='2012-01-01')
        transactions = utils.filter_transactions(company, end_period=period[1])

        discount = factories.DiscountFactory()
        discount_transactions = utils.get_discount_transactions(transactions)

        self.assertEqual(unicode(discount_transactions[0].discount), unicode(discount.discount))
        self.assertEqual(unicode(discount_transactions[1].discount), unicode(discount.discount))
        self.assertEqual(discount_transactions[2].discount, 0.00)

    def test_discount_transactions_without_discount(self):
        company = factories.CompanyFactory(title='Neftehim')
        period = ['2010-01-01', '2012-01-01']

        factories.CardTransactionFactory(card_holder__company=company, volume=10, price=22, made_at='2011-01-01')
        factories.CardTransactionFactory(card_holder__company=company, volume=10, price=23.80, made_at='2011-01-02')
        factories.CardTransactionFactory(card_holder__company=company, volume=100, price=23.80, made_at='2012-01-01')
        transactions = utils.filter_transactions(company, end_period=period[1])

        factories.DiscountFactory()

        discount_transactions = utils.get_discount_transactions(transactions)

        self.assertEqual(discount_transactions[0].discount, 0.00)
        self.assertEqual(discount_transactions[1].discount, 0.00)
        self.assertEqual(discount_transactions[2].discount, 0.00)

    def test_discount_transaction(self):
        company = factories.CompanyFactory()
        period = ['2010-01-01', '2012-01-01']
        factories.CardTransactionFactory(card_holder__company=company, volume=10, price=22, made_at='2011-01-01')

        transactions = utils.filter_transactions(company, end_period=period[1])
        discount = factories.DiscountFactory()
        discount_transactions = utils.get_discount_transactions(transactions)

        self.assertEqual(unicode(discount_transactions[0].discount), unicode(discount.discount))

    def test_summary_data_counting(self):
        company = factories.CompanyFactory()
        period = ['2010-01-01', '2012-01-01']

        factories.CardTransactionFactory(card_holder__company=company, volume=10, price=22, made_at='2011-01-01')
        factories.CardTransactionFactory(card_holder__company=company, volume=10, price=22, made_at='2011-02-01', fuel=u'92')
        factories.CardTransactionFactory(card_holder__company=company, volume=10, price=22, made_at='2011-03-01')
        factories.DiscountFactory()
        transactions = utils.filter_transactions(company, start_period=period[0], end_period=period[1])

        summary_data = utils.get_summary_data(transactions)

        self.assertEqual(summary_data['total'], 660)
        self.assertEqual(summary_data['saved_money'], Decimal('2.2000'))
        self.assertEqual(len(summary_data['fuel']), 2)
        self.assertEqual(summary_data['fuel'][u'92'], 10)
        self.assertEqual(summary_data['fuel'][u'DT'], 20)









