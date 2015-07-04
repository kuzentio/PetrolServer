# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import models as auth_models


class User(models.Model):
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    user = models.OneToOneField(auth_models.User)
    sms_telephone = models.CharField(max_length=13, blank=True)
    fax_telephone = models.CharField(max_length=13, blank=True)

    def __unicode__(self):
        return unicode(self.user)


class Company(models.Model):
    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    title = models.CharField(max_length=100, verbose_name='Название')
    user = models.ForeignKey(User, verbose_name='Пользователь')

    def __unicode__(self):
        return unicode(self.title)


class Card(models.Model):
    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    number = models.CharField(max_length=15, verbose_name='Номер карты')

    def __unicode__(self):
        return unicode(self.number)


class PetrolStation(models.Model):
    class Meta:
        verbose_name = 'АЗС'
        verbose_name_plural = 'АЗС'
    address = models.CharField(max_length=200, verbose_name='Адрес')

    def __unicode__(self):
        return unicode(self.address)


class Cardholder(models.Model):
    class Meta:
        verbose_name = 'Держатель'
        verbose_name_plural = 'Держатели'

    card = models.ForeignKey(Card, verbose_name='Карта')
    company = models.ForeignKey(Company, verbose_name='Компания')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __unicode__(self):
        return u'%s - %s' % (self.card, self.company)


class CardTransaction(models.Model):
    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    made_at = models.DateField(verbose_name='Дата')

    card = models.ForeignKey(Card, verbose_name='Карта')

    card_holder = models.ForeignKey(Cardholder, verbose_name='Держатель')
    petrol_station = models.ForeignKey(PetrolStation, verbose_name='АЗС')

    fuel = models.CharField(max_length=300, verbose_name='Вид топлива')
    volume = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Количество')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')

    is_approved = models.BooleanField(default=False, verbose_name='Проведен')
    is_no_need_attention = models.BooleanField(default=True, verbose_name='Обратить внимание')


class Payment(models.Model):
    class Meta:
        verbose_name = 'Платежи'
        verbose_name_plural = 'Платежи'

    company = models.ForeignKey(Company)
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Сумма')
    date = models.DateTimeField(editable=True, verbose_name='Дата')

    def __unicode__(self):
        return u'%s - %s' % (self.amount, self.company)


class Discount(models.Model):
    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    company = models.ForeignKey(Company)
    discount = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Скидка')
    date_from = models.DateField(verbose_name='Начальная дата')
    date_to = models.DateField(verbose_name='Конечная дата')

    def __unicode__(self):
        return u'%s - %s (%s - %s)' % (self.company, self.discount, self.date_from, self.date_to)


