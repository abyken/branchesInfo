# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branchesInfo', '0002_auto_20160812_0253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='address',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='branchNumber',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='city',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='lat',
            field=models.DecimalField(null=True, max_digits=15, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='lng',
            field=models.DecimalField(null=True, max_digits=15, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='break',
            name='time_from',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='break',
            name='time_to',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='time_from',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='time_to',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
