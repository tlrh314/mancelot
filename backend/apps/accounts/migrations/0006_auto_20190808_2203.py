# Generated by Django 2.2.4 on 2019-08-08 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20190807_2221'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usermodel',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='date Laatst Gewijzigd'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='saved_by_users', to='catalogue.Product', verbose_name='favorites'),
        ),
    ]
