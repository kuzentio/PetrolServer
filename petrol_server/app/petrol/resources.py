# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_text
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DateWidget
from petrol_server.app.petrol import models


class CustomModelInstanceLoader(resources.ModelInstanceLoader):
    def get_instance(self, row):
        return None


class CustomForeignKeyWidget(ForeignKeyWidget):

    def clean(self, value):
        try:
            return super(CustomForeignKeyWidget, self).clean(value)
        except ObjectDoesNotExist:
            return models.PetrolStation.objects.create(address=value)


class TransactionResource(resources.ModelResource):
    card = fields.Field(
        column_name='card',
        attribute="card",
        widget=ForeignKeyWidget(models.Card, 'number'),
    )

    petrol_station = fields.Field(
        column_name='petrol_station',
        attribute="petrol_station",
        widget=CustomForeignKeyWidget(models.PetrolStation, 'address'),
    )

    made_at = fields.Field(
        column_name='made_at',
        attribute="made_at",
        widget=DateWidget(format='%d.%m.%Y')
    )

    fuel = fields.Field(
        column_name='fuel',
        attribute="fuel"
    )
    volume = fields.Field(
        column_name='volume',
        attribute="volume"
    )
    price = fields.Field(
        column_name='price',
        attribute="price"
    )

    class Meta:
        model = models.CardTransaction

        instance_loader_class = CustomModelInstanceLoader
        fields = ('made_at', 'card', 'petrol_station', 'fuel', 'volume', 'price',)
        exclude = ('id',)
        import_id_fields = ['made_at', 'card', 'azs', 'fuel', 'volume', 'price']
        widgets = {
                'made_at': {'format': '%d.%m.%Y'},
                }
