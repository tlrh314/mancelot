# Generated by Django 2.2.4 on 2019-08-06 22:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import filebrowser.fields
import jsonfield.fields
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogue', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'verbose_name': 'Merk', 'verbose_name_plural': 'Merken'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Categorie', 'verbose_name_plural': 'Categorieën'},
        ),
        migrations.AlterModelOptions(
            name='cecelabel',
            options={'verbose_name': 'Label', 'verbose_name_plural': 'Labels'},
        ),
        migrations.AlterModelOptions(
            name='certificate',
            options={'verbose_name': 'Certificaat', 'verbose_name_plural': 'Certificaten'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Producten'},
        ),
        migrations.AlterModelOptions(
            name='store',
            options={'verbose_name': 'Winkel', 'verbose_name_plural': 'Winkels'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name': 'Subcategorie', 'verbose_name_plural': 'Subcategorie'},
        ),
        migrations.AddField(
            model_name='brand',
            name='cece_api_url',
            field=models.URLField(blank=True, null=True, verbose_name='cece_api_url'),
        ),
        migrations.AddField(
            model_name='brand',
            name='certificate',
            field=models.ManyToManyField(blank=True, related_name='brands', to='catalogue.Certificate'),
        ),
        migrations.AddField(
            model_name='brand',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Datum Aangemaakt'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brand',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Datum Laatst Gewijzigd'),
        ),
        migrations.AddField(
            model_name='brand',
            name='labels',
            field=models.ManyToManyField(blank=True, related_name='brands', to='catalogue.CeceLabel'),
        ),
        migrations.AddField(
            model_name='brand',
            name='last_updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_changed_brand', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='brand',
            name='logo',
            field=filebrowser.fields.FileBrowseField(default='/static/img/test/test_logo.png', max_length=200, verbose_name='logo'),
        ),
        migrations.AddField(
            model_name='brand',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='url'),
        ),
        migrations.AddField(
            model_name='category',
            name='cece_api_url',
            field=models.URLField(blank=True, null=True, verbose_name='cece_api_url'),
        ),
        migrations.AddField(
            model_name='category',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Datum Aangemaakt'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Datum Laatst Gewijzigd'),
        ),
        migrations.AddField(
            model_name='category',
            name='last_updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_changed_category', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='section',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Mannen'), (1, 'Vrouwen'), (1, 'Kinderen')], default=0, verbose_name='sectie'),
        ),
        migrations.AddField(
            model_name='cecelabel',
            name='cece_api_url',
            field=models.URLField(blank=True, null=True, verbose_name='cece_api_url'),
        ),
        migrations.AddField(
            model_name='cecelabel',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Datum Aangemaakt'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cecelabel',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Datum Laatst Gewijzigd'),
        ),
        migrations.AddField(
            model_name='cecelabel',
            name='last_updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_changed_cecelabel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='certificate',
            name='cece_api_url',
            field=models.URLField(blank=True, null=True, verbose_name='cece_api_url'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Datum Aangemaakt'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='certificate',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Datum Laatst Gewijzigd'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='last_updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_changed_certificate', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(default=42, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='catalogue.Brand'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='products', to='catalogue.Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='cece_api_url',
            field=models.URLField(blank=True, null=True, verbose_name='cece_api_url'),
        ),
        migrations.AddField(
            model_name='product',
            name='cece_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='cece product id'),
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='kleur'),
        ),
        migrations.AddField(
            model_name='product',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Datum Aangemaakt'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Datum Laatst Gewijzigd'),
        ),
        migrations.AddField(
            model_name='product',
            name='extra_images',
            field=jsonfield.fields.JSONField(blank=True, verbose_name='extra afbeeldingen'),
        ),
        migrations.AddField(
            model_name='product',
            name='extra_info',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='extra info'),
        ),
        migrations.AddField(
            model_name='product',
            name='from_price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Product is in de aanbieding als er een originele is.', max_digits=6, null=True, verbose_name='originele prijs'),
        ),
        migrations.AddField(
            model_name='product',
            name='info',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='info'),
        ),
        migrations.AddField(
            model_name='product',
            name='last_updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_changed_product', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='main_image',
            field=models.URLField(default='/static/img/test/test_logo.png', max_length=450, verbose_name='hoofdafbeelding'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=42, max_digits=6, verbose_name='prijs'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='store',
            field=models.ForeignKey(default=42, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='catalogue.Store'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ManyToManyField(blank=True, related_name='products', to='catalogue.Subcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='url',
            field=models.URLField(default='/static/img/test/test_logo.png', verbose_name='url'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='store',
            name='address',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Straatnaam huisnummer'),
        ),
        migrations.AddField(
            model_name='store',
            name='cece_api_url',
            field=models.URLField(blank=True, null=True, verbose_name='cece_api_url'),
        ),
        migrations.AddField(
            model_name='store',
            name='city',
            field=models.CharField(blank=True, max_length=42, null=True, verbose_name='Stad'),
        ),
        migrations.AddField(
            model_name='store',
            name='country',
            field=django_countries.fields.CountryField(blank=True, default='NL', max_length=2, null=True, verbose_name='Land'),
        ),
        migrations.AddField(
            model_name='store',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Datum Aangemaakt'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='store',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Datum Laatst Gewijzigd'),
        ),
        migrations.AddField(
            model_name='store',
            name='last_updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_changed_store', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='store',
            name='logo',
            field=filebrowser.fields.FileBrowseField(default='/static/img/test/test_logo.png', max_length=200, verbose_name='logo'),
        ),
        migrations.AddField(
            model_name='store',
            name='url',
            field=models.URLField(default='/static/img/test/test_logo.png', verbose_name='url'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='store',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Postcode'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='cece_api_url',
            field=models.URLField(blank=True, null=True, verbose_name='cece_api_url'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Datum Aangemaakt'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subcategory',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Datum Laatst Gewijzigd'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='last_updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_changed_subcategory', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='brand',
            name='info',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='info'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=200, verbose_name='naam'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=200, verbose_name='naam'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='cecelabel',
            name='info',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='info'),
        ),
        migrations.AlterField(
            model_name='cecelabel',
            name='name',
            field=models.CharField(max_length=200, verbose_name='naam'),
        ),
        migrations.AlterField(
            model_name='cecelabel',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='info',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='info'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='name',
            field=models.CharField(max_length=200, verbose_name='naam'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, verbose_name='naam'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='store',
            name='info',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='info'),
        ),
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(max_length=200, verbose_name='naam'),
        ),
        migrations.AlterField(
            model_name='store',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='catalogue.Category'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(max_length=200, verbose_name='naam'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug'),
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='naam')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug')),
                ('cece_api_url', models.URLField(blank=True, null=True, verbose_name='cece_api_url')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Datum Aangemaakt')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Datum Laatst Gewijzigd')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_changed_size', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Maat',
                'verbose_name_plural': 'Maten',
            },
        ),
        migrations.CreateModel(
            name='PaymentOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='naam')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug')),
                ('logo', filebrowser.fields.FileBrowseField(default='/static/img/test/test_logo.png', max_length=200, verbose_name='logo')),
                ('cece_api_url', models.URLField(blank=True, null=True, verbose_name='cece_api_url')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Datum Aangemaakt')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Datum Laatst Gewijzigd')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_changed_paymentoption', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Betaalmethode',
                'verbose_name_plural': 'Betaalmethodes',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='naam')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug')),
                ('info', tinymce.models.HTMLField(blank=True, null=True, verbose_name='info')),
                ('cece_api_url', models.URLField(blank=True, null=True, verbose_name='cece_api_url')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Datum Aangemaakt')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Datum Laatst Gewijzigd')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_changed_material', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Materiaal',
                'verbose_name_plural': 'Materialen',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='material',
            field=models.ManyToManyField(blank=True, related_name='products', to='catalogue.Material'),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(blank=True, related_name='products', to='catalogue.Size'),
        ),
        migrations.AddField(
            model_name='store',
            name='payment_options',
            field=models.ManyToManyField(related_name='stores', to='catalogue.PaymentOption'),
        ),
    ]