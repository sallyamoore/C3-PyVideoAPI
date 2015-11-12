# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20151110_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='num_available',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
