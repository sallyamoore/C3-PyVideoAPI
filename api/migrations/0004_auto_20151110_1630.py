# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20151110_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(1)]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='city',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(1)]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(7)]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='postal_code',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(1)]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='state',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(1)]),
        ),
    ]
