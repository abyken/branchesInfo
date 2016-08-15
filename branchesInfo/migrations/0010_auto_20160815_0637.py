# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branchesInfo', '0009_auto_20160812_0930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='isAroundTheClock',
        ),
        migrations.AddField(
            model_name='branch',
            name='isAroundTheClock',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='branch',
            name='type',
            field=models.CharField(default='BRANCH', max_length=10, choices=[('BRANCH', 'Branch'), ('ATM', 'Atm'), ('TERMINAL', 'Terminal')]),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='type',
            field=models.CharField(default='WD', max_length=2, choices=[('WD', 'Working day'), ('SD', 'Short day')]),
        ),
    ]
