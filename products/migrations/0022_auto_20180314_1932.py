# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-14 14:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_auto_20180314_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='specs_line_1',
            field=models.CharField(default='Line 1', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='specs_line_2',
            field=models.CharField(default='Line 2', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='specs_line_3',
            field=models.CharField(default='Line 3', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='specs_line_4',
            field=models.CharField(default='Line 4', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='specs_line_5',
            field=models.CharField(default='Line 5', max_length=50),
        ),
    ]
