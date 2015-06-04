
from factory import DjangoModelFactory
import factory
from petrol_server.app.petrol import models
from django.contrib.auth import models as auth_models


class DjangoUserFactory(DjangoModelFactory):
    class Meta:
        model = auth_models.User
        django_get_or_create = ('username',)
    username = 'Bill'


class UserFactory(DjangoModelFactory):
    class Meta:
        model = models.User
        django_get_or_create = ('user',)
    user = factory.SubFactory(DjangoUserFactory)


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = models.Company
        django_get_or_create = ('title', 'user',)
    title = 'Hozhm'
    user = factory.SubFactory(UserFactory)


class CardFactory(DjangoModelFactory):
    class Meta:
        model = models.Card
        django_get_or_create = ('number',)
    number = 123


class CardHolderFactory(DjangoModelFactory):
    class Meta:
        model = models.Cardholder
        django_get_or_create = ('card', 'company',)
    card = factory.SubFactory(CardFactory)
    company = factory.SubFactory(CompanyFactory)


class PetrolStationFactory(DjangoModelFactory):
    class Meta:
        model = models.PetrolStation
        django_get_or_create = ('address',)
    address = 'Kiev, Kievskaya str.'


class CardTransactionFactory(DjangoModelFactory):
    class Meta:
        model = models.CardTransaction
        django_get_or_create = ('card',
                                'made_at',
                                'card_holder',
                                'petrol_station',
                                'fuel', 'volume',
                                'price', 'is_approved',
                                'is_no_need_attention')
    made_at = '2011-01-01'
    card = factory.SubFactory(CardFactory)
    card_holder = factory.SubFactory(CardHolderFactory)
    petrol_station = factory.SubFactory(PetrolStationFactory)
    fuel = 'DT'
    volume = 10
    price = 20
    is_approved = False
    is_no_need_attention = False


class PaymentsFactory(DjangoModelFactory):
    class Meta:
        model = models.Payment
        django_get_or_create = ('company', 'amount', 'date',)
    company = factory.SubFactory(CompanyFactory)
    amount = 1000
    date = '2011-01-01'



