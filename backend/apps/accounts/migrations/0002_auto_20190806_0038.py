# Generated by Django 2.2.4 on 2019-08-05 22:38

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='address',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='city',
            field=models.CharField(blank=True, max_length=42, null=True, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='country',
            field=django_countries.fields.CountryField(blank=True, default='NL', max_length=2, null=True, verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='full_name',
            field=models.CharField(max_length=42, null=True, verbose_name='Full Name'),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Zip Code'),
        ),
    ]
