# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branchesInfo', '0012_auto_20160815_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='isLimitedAccess',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='branch',
            name='access',
            field=models.CharField(default='UNLIMITED', max_length=10, choices=[('LIMITED', '\u041e\u0433\u0440\u0430\u043d\u0438\u0447\u0435\u043d\u043d\u044b\u0439'), ('UNLIMITED', '\u041d\u0435\u043e\u0433\u0440\u0430\u043d\u0438\u0447\u0435\u043d\u043d\u044b\u0439')]),
        ),
        migrations.AlterField(
            model_name='branch',
            name='clients',
            field=models.CharField(default='INDIVIDUAL', max_length=10, choices=[('INDIVIDUAL', '\u0424\u0438\u0437. \u043b\u0438\u0446\u0430'), ('CORPORATION', '\u042e\u0440. \u043b\u0438\u0446\u0430'), ('BOTH', '\u0424\u0438\u0437. \u043b\u0438\u0446\u0430/\u042e\u0440. \u043b\u0438\u0446\u0430"')]),
        ),
    ]
