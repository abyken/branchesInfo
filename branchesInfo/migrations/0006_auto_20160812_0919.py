# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branchesInfo', '0005_branch_isempty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('day', models.CharField(unique=True, max_length=10, choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='day',
        ),
        migrations.AddField(
            model_name='schedule',
            name='type',
            field=models.CharField(default='QD', max_length=2, choices=[('QD', 'Working day'), ('SD', 'Short day'), ('DO', 'Day off')]),
        ),
        migrations.AddField(
            model_name='schedule',
            name='days',
            field=models.ManyToManyField(related_name='schedule', to='branchesInfo.Day', blank=True),
        ),
    ]
