# Generated by Django 2.2.4 on 2019-08-10 11:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogue', '0006_auto_20190808_2203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'verbose_name': 'Brand', 'verbose_name_plural': 'Brands'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='catalogue.Brand', verbose_name='brand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(related_name='products', to='catalogue.Category', verbose_name='categories'),
        ),
        migrations.AlterField(
            model_name='product',
            name='materials',
            field=models.ManyToManyField(blank=True, related_name='products', to='catalogue.Material', verbose_name='materials'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(blank=True, related_name='products', to='catalogue.Size', verbose_name='sizes'),
        ),
        migrations.AlterField(
            model_name='product',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='catalogue.Store', verbose_name='store'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategories',
            field=models.ManyToManyField(blank=True, related_name='products', to='catalogue.Subcategory', verbose_name='subcategories'),
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug')),
                ('cece_api_url', models.URLField(blank=True, null=True, verbose_name='cece_api_url')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_changed_color', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Color',
                'verbose_name_plural': 'Colors',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(blank=True, related_name='products', to='catalogue.Color', verbose_name='colors'),
        ),
    ]
