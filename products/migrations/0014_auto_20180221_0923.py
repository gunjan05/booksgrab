# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-21 03:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_product_percent_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='percent_discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4),
        ),
    ]
