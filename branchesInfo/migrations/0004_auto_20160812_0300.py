# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branchesInfo', '0003_auto_20160812_0255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='branchBreak',
            field=models.ForeignKey(related_name='branches', blank=True, to='branchesInfo.Break'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='currencies',
            field=models.ManyToManyField(related_name='branches', to='branchesInfo.Currency', blank=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='schedule',
            field=models.ManyToManyField(related_name='branches', to='branchesInfo.Schedule', blank=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='services',
            field=models.ManyToManyField(related_name='branches', to='branchesInfo.Service', blank=True),
        ),
    ]
