# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import api.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('registered_at', models.DateTimeField()),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('account_credit', models.DecimalField(max_digits=7, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('overview', models.TextField()),
                ('release_date', models.DateTimeField()),
                ('inventory', models.PositiveSmallIntegerField()),
                ('num_available', models.PositiveSmallIntegerField(validators=[api.models.validate_num_available])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('checkout_date', models.DateTimeField()),
                ('return_date', models.DateTimeField()),
                ('checked_out', models.BooleanField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(to='api.Customer', on_delete=django.db.models.deletion.DO_NOTHING)),
                ('movie', models.ForeignKey(to='api.Movie', on_delete=django.db.models.deletion.DO_NOTHING)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='members',
            field=models.ManyToManyField(to='api.Customer', through='api.Rental'),
        ),
    ]
