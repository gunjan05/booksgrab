# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-24 14:17
from __future__ import unicode_literals

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20180224_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, unique=True),
        ),
    ]
