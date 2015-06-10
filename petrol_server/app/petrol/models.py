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
    number = models.CharField(max_length=15)

    def __unicode__(self):
        return unicode(self.number)


class PetrolStation(models.Model):
    address = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.address)


class Cardholder(models.Model):
    card = models.ForeignKey(Card)
    company = models.ForeignKey(Company)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s - %s' % (self.card, self.company)


class CardTransaction(models.Model):
    made_at = models.DateField()

    card = models.ForeignKey(Card)

    card_holder = models.ForeignKey(Cardholder)
    petrol_station = models.ForeignKey(PetrolStation)

    fuel = models.CharField(max_length=300)
    volume = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    is_approved = models.BooleanField(default=False)
    is_no_need_attention = models.BooleanField(default=True)


class Payment(models.Model):
    company = models.ForeignKey(Company)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateTimeField(editable=True)

    def __unicode__(self):
        return u'%s - %s' % (self.amount, self.company)

