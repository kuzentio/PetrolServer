# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_text
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DateWidget
from petrol_server.app.petrol import models


class CustomModelInstanceLoader(resources.ModelInstanceLoader):

    def get_instance(self, row):
        return None


class PetrolStationWidget(ForeignKeyWidget):

    def clean(self, value):
        try:
            return super(PetrolStationWidget, self).clean(value)
        except ObjectDoesNotExist:
            return models.PetrolStation.objects.create(address=value)


class TransactionResource(resources.ModelResource):

    card = fields.Field(
        column_name=u'карта',
        attribute="card",
        widget=ForeignKeyWidget(model=models.Card, field='number'),
    )

    petrol_station = fields.Field(
        column_name=u'адрес азс',
        attribute="petrol_station",
        widget=PetrolStationWidget(model=models.PetrolStation, field='address'),
    )

    made_at = fields.Field(
        column_name=u'Дата',
        attribute="made_at",
        widget=DateWidget(format='%d.%m.%Y')
    )

    fuel = fields.Field(
        column_name=u'вид топлива',
        attribute="fuel"
    )
    volume = fields.Field(
        column_name=u'кол-во',
        attribute="volume"
    )
    price = fields.Field(
        column_name=u'цена без скидки',
        attribute="price"
    )
    #card_holder = fields.Field()


    class Meta:

        model = models.CardTransaction

        instance_loader_class = CustomModelInstanceLoader
        fields = ('made_at', 'card', 'petrol_station', 'fuel', 'volume', 'price',)
        exclude = ('id',)
        import_id_fields = ['made_at', 'card', 'azs', 'fuel', 'volume', 'price',]

    def before_save_instance(self, instance, dry_run):
        instance.card_holder = models.Cardholder.objects.filter(card=instance.card).latest('date')
        if instance.volume <= 0:
            instance.is_no_need_attention=False
