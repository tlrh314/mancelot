# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 12:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0002_auto_20170226_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='Google_Authenticator',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=256, verbose_name='title')),
                ('secret', models.CharField(max_length=1024, verbose_name='secret as hex')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='google_authenticator', to='restapi.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='token',
            name='google_authenticator_2fa',
            field=models.BooleanField(default=False, help_text='Specifies if Google Authenticator is required or not', verbose_name='Google Authenticator Required'),
        ),
    ]
