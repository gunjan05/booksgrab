# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-21 03:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_product_display_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='percent_discount',
            field=models.CharField(default='0% off', max_length=10),
        ),
    ]
