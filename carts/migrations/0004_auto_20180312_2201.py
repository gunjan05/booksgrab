# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-12 16:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_paymentdetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentdetails',
            name='cart',
        ),
        migrations.DeleteModel(
            name='PaymentDetails',
        ),
    ]
