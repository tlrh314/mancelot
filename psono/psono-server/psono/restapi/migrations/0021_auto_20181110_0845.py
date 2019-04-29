# Generated by Django 2.1 on 2018-11-10 08:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0020_secret_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emergency_Code',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('emergency_authkey', models.CharField(max_length=128, verbose_name='emergency auth key')),
                ('emergency_data', models.BinaryField()),
                ('emergency_data_nonce', models.CharField(max_length=64, unique=True, verbose_name='emergency data nonce')),
                ('verifier', models.CharField(max_length=256, verbose_name='last verifier')),
                ('verifier_issue_date', models.DateTimeField(blank=True, null=True)),
                ('emergency_sauce', models.CharField(max_length=64, verbose_name='user sauce')),
                ('description', models.CharField(max_length=256, null=True)),
                ('activation_delay', models.PositiveIntegerField(verbose_name='Delay till activation in seconds')),
                ('activation_date', models.DateTimeField(blank=True, null=True, verbose_name='Date this emergency code becomes active')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emergency_code', to='restapi.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='token',
            name='is_emergency_session',
            field=models.BooleanField(default=False, help_text='Specifies if the token has been created with an emergency code or not', verbose_name='Is an emergency session'),
        ),
    ]