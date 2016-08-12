# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branchesInfo', '0006_auto_20160812_0919'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='isDayOff',
            new_name='isAroundTheClock',
        ),
    ]
