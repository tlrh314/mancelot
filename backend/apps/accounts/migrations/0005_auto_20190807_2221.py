# Generated by Django 2.2.4 on 2019-08-07 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190807_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='full_name',
            field=models.CharField(max_length=150, null=True, verbose_name='Volledige naam'),
        ),
    ]