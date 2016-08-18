# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branchesInfo', '0014_break_isflexible'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'ordering': ('-date_created',), 'verbose_name_plural': 'Branches'},
        ),
        migrations.RemoveField(
            model_name='branch',
            name='isLimitedAccess',
        ),
    ]
