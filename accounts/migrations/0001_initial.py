# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-31 03:35
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(default='abc123@gmail.com', max_length=255, unique=True)),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(default='9999999999', max_length=128)),
                ('first_name', models.CharField(default='John', max_length=255)),
                ('last_name', models.CharField(default='Miller', max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GuestDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(default='9999999999', max_length=128)),
                ('first_name', models.CharField(default='John', max_length=255)),
                ('last_name', models.CharField(default='Miller', max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
