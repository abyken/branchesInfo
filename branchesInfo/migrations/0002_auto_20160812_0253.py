# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branchesInfo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'verbose_name_plural': 'Branches'},
        ),
        migrations.AlterModelOptions(
            name='currency',
            options={'verbose_name_plural': 'Currencies'},
        ),
        migrations.AlterField(
            model_name='break',
            name='time_from',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='break',
            name='time_to',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
