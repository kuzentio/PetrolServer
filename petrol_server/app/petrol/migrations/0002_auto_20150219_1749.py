# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('petrol', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='number',
            field=models.DecimalField(max_digits=20, decimal_places=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cardtransaction',
            name='volume',
            field=models.DecimalField(max_digits=6, decimal_places=2),
            preserve_default=True,
        ),
    ]
