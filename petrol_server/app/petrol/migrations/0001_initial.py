# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CardTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fuel', models.CharField(max_length=300)),
                ('volume', models.FloatField()),
                ('price', models.DecimalField(max_digits=8, decimal_places=2)),
                ('made_at', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PetrolStation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('azs_address', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='company',
            name='users',
            field=models.ManyToManyField(to='petrol.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardtransaction',
            name='azs',
            field=models.ForeignKey(to='petrol.PetrolStation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardtransaction',
            name='card',
            field=models.ForeignKey(to='petrol.Card'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='company',
            field=models.ForeignKey(to='petrol.Company'),
            preserve_default=True,
        ),
    ]
