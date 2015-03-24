import datetime
from django.db import models
from django.contrib.auth import models as auth_models


class User(models.Model):
    user = models.OneToOneField(auth_models.User)
    sms_telephone = models.CharField(max_length=13, blank=True)
    fax_telephone = models.CharField(max_length=13, blank=True)

    def __unicode__(self):
        return unicode(self.user)


class Company(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(self.title)


class Card(models.Model):
    number = models.DecimalField(max_digits=20, decimal_places=0)

    def __unicode__(self):
        return unicode(self.number)


class PetrolStation(models.Model):
    address = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.address)


class CurrentCardHolder(models.Model):
    card = models.ForeignKey(Card)
    company = models.ForeignKey(Company)
    date = models.DateField(default=datetime.date.today)
    def __unicode__(self):
        return u'%s - %s' % (self.card, self.company)


class CardTransaction(models.Model):
    #FUEL_DT, FUEL_92, FUEL_95 = range(3)
    #CHOICES_STATUS = [
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

    is_approved = models.BooleanField(default=False)
    is_no_need_attention = models.BooleanField(default=True)


    #def __unicode__(self):
    #    return unicode(self.made_at)

