# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-18 14:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billingprofile',
            old_name='updated',
            new_name='update',
        ),
    ]
