# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-21 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_product_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='short_description',
            field=models.CharField(default='A Short Description Of the Book', max_length=20),
        ),
    ]
