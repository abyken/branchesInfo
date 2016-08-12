# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branchesInfo', '0004_auto_20160812_0300'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='isEmpty',
            field=models.BooleanField(default=True),
        ),
    ]
