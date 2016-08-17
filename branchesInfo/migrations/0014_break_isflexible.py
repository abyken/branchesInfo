# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branchesInfo', '0013_auto_20160817_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='break',
            name='isFlexible',
            field=models.BooleanField(default=False),
        ),
    ]
