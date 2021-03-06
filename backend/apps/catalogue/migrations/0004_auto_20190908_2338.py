# Generated by Django 2.2.5 on 2019-09-08 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_auto_20190822_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='active',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, verbose_name='active'),
        ),
        migrations.AddField(
            model_name='category',
            name='active',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, verbose_name='active'),
        ),
        migrations.AddField(
            model_name='store',
            name='active',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, verbose_name='active'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='active',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, verbose_name='active'),
        ),
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, verbose_name='active'),
        ),
    ]
