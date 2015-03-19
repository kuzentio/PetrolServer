from unittest import TestCase
from petrol_server.app.petrol.test import factories


class TestPeriodForm(TestCase):
    def test_test(self):
        user = factories.UserFactory.create()
        company = factories.CompanyFactory.create()
        card = factories.CardFactory.create()
        petrol_station = factories.PetrolStationFactory.create()
        card_transaction = factories.CardTransactionFactory.create()
        self.assertEquals(user.username, 'test')
        self.assertEquals(company.title, 'TestCorp')
        self.assertEquals(card.number, '1234567890')
        self.assertEquals(petrol_station.address, 'Kiev')
        self.assertEquals(card_transaction.made_at, '1.01.2014')