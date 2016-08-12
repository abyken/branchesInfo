# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branchesInfo', '0008_auto_20160812_0927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='day',
            old_name='day',
            new_name='name',
        ),
    ]
