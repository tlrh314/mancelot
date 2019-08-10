# Generated by Django 2.2.4 on 2019-08-10 14:53

from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20190810_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='balance',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=4, default_currency='EUR', max_digits=19, null=True, verbose_name='balance'),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='balance_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €'), ('GBP', 'GBP £'), ('USD', 'USD $')], default='EUR', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='monthly_top_up',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=4, default_currency='EUR', max_digits=19, null=True, verbose_name='monthly top up'),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='monthly_top_up_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €'), ('GBP', 'GBP £'), ('USD', 'USD $')], default='EUR', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='payment_preference',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Bank Transfer'), (1, 'Ideal'), (2, 'Paypal')], default=None, null=True, verbose_name='payment preference'),
        ),
    ]
