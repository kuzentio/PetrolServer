from django.contrib.auth.models import User
import factory
from petrol_server.app.petrol import models


class UserFactory(factory.Factory):
    FACTORY_FOR = User
    username = 'test'
    password = '1'


class CompanyFactory(factory.Factory):
    FACTORY_FOR = models.Company
    title = 'TestCorp'



class CardFactory(factory.Factory):
    FACTORY_FOR = models.Card
    number = '1234567890'
    company = factory.SubFactory(CompanyFactory)


class PetrolStationFactory(factory.Factory):
    FACTORY_FOR = models.PetrolStation
    address = 'Kiev'


class CardTransactionFactory(factory.Factory):
    FACTORY_FOR = models.CardTransaction
    made_at = '1.01.2014'
    card = factory.SubFactory(CardFactory)
    petrol_station = factory.SubFactory(PetrolStationFactory)
    fuel = 'DT'
    volume = '100'
    price = '12'
