# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branchesInfo', '0011_auto_20160815_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='access',
            field=models.CharField(default='UNLIMITED', max_length=10, choices=[('LIMITED', '\u041d\u0435\u043e\u0433\u0440\u0430\u043d\u0438\u0447\u0435\u043d\u043d\u044b\u0439'), ('UNLIMITED', '\u041f\u0440\u043e\u043f\u0443\u0441\u043a\u043d\u0430\u044f \u0441\u0438\u0441\u0442\u0435\u043c\u0430')]),
        ),
        migrations.AlterField(
            model_name='branch',
            name='type',
            field=models.CharField(default='branch', max_length=10, choices=[('branch', '\u041e\u0442\u0434\u0435\u043b\u0435\u043d\u0438\u0435'), ('atm', '\u0411\u0430\u043d\u043a\u043e\u043c\u0430\u0442'), ('kiosk', '\u0422\u0435\u0440\u043c\u0438\u043d\u0430\u043b')]),
        ),
    ]
