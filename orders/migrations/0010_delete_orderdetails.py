# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-15 15:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_orderdetails'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderDetails',
        ),
    ]
