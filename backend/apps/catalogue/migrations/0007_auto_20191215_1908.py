# Generated by Django 2.2.8 on 2019-12-15 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_auto_20191103_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoriteproduct',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favorites', to='catalogue.Size', verbose_name='size'),
        ),
        migrations.AddField(
            model_name='product',
            name='chosen_image',
            field=models.URLField(blank=True, max_length=450, null=True, verbose_name='chosen  image'),
        ),
    ]