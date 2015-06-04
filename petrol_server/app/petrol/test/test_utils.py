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

    #TODO: Write test for balance on date
