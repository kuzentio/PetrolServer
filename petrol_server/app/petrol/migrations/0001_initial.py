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
                ('number', models.DecimalField(max_digits=20, decimal_places=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cardholder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('card', models.ForeignKey(to='petrol.Card')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CardTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('made_at', models.DateField()),
                ('fuel', models.CharField(max_length=300)),
                ('volume', models.DecimalField(max_digits=6, decimal_places=2)),
                ('price', models.DecimalField(max_digits=8, decimal_places=2)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_no_need_attention', models.BooleanField(default=True)),
                ('card', models.ForeignKey(to='petrol.Card')),
                ('card_holder', models.ForeignKey(to='petrol.Cardholder')),
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
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(max_digits=20, decimal_places=2)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(to='petrol.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PetrolStation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sms_telephone', models.CharField(max_length=13, blank=True)),
                ('fax_telephone', models.CharField(max_length=13, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.ForeignKey(to='petrol.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardtransaction',
            name='petrol_station',
            field=models.ForeignKey(to='petrol.PetrolStation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardholder',
            name='company',
            field=models.ForeignKey(to='petrol.Company'),
            preserve_default=True,
        ),
    ]
