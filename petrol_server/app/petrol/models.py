from django.db import models
from django.contrib.auth import models as auth_models


class User(models.Model):
    user = models.OneToOneField(auth_models.User)
    def __unicode__(self):
        return unicode(self.user)


class Company(models.Model):
    title = models.CharField(max_length=100)
    users = models.ManyToManyField(User)
    def __unicode__(self):
        return unicode(self.title)


class Card(models.Model):
    number = models.DecimalField(max_digits=20, decimal_places=0)
    company = models.ForeignKey(Company)
    def __unicode__(self):
        return unicode(self.number)


class PetrolStation(models.Model):
    address = models.CharField(max_length=200)


class CardTransaction(models.Model):
    #FUEL_DT, FUEL_92, FUEL_95 = range(3)
    #FUEL_CHOICES = [
    #    (FUEL_DT, 'dt'),
    #    (FUEL_92, '92'),
    #    (FUEL_95, '95'),
    #]
    made_at = models.DateField()

    card = models.ForeignKey(Card)
    petrol_station = models.ForeignKey(PetrolStation)

    fuel = models.CharField(max_length=300)
    volume = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2)

