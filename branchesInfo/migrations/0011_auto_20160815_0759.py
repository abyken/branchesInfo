# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branchesInfo', '0010_auto_20160815_0637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='type',
            field=models.CharField(default='branch', max_length=10, choices=[('branch', 'Branch'), ('atm', 'Atm'), ('terminal', 'Terminal')]),
        ),
    ]
