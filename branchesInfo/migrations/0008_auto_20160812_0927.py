# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branchesInfo', '0007_auto_20160812_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='type',
            field=models.CharField(default='WD', max_length=2, choices=[('WD', 'Working day'), ('SD', 'Short day'), ('DO', 'Day off')]),
        ),
    ]
