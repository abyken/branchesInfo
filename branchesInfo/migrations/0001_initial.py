# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('isActive', models.BooleanField(default=True)),
                ('type', models.CharField(default='BRANCH', max_length=10, choices=[('BRANCH', 'Branch'), ('ATM', 'Atm'), ('ATM24', 'Atm24'), ('TERMINAL', 'Terminal')])),
                ('isCashIn', models.BooleanField(default=False)),
                ('lat', models.DecimalField(null=True, max_digits=15, decimal_places=6)),
                ('lng', models.DecimalField(null=True, max_digits=15, decimal_places=6)),
                ('branchNumber', models.IntegerField(null=True)),
                ('city', models.CharField(max_length=1024)),
                ('name', models.CharField(max_length=1024)),
                ('address', models.CharField(max_length=1024)),
                ('clients', models.CharField(default='INDIVIDUAL', max_length=10, choices=[('INDIVIDUAL', 'Individual'), ('CORPORATION', 'Corporation'), ('BOTH', 'Individual/Corporation')])),
                ('access', models.CharField(default='UNLIMITED', max_length=10, choices=[('LIMITED', 'Limited entrance'), ('UNLIMITED', 'Unlimited entance')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Break',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('time_from', models.CharField(max_length=50)),
                ('time_to', models.CharField(max_length=50)),
                ('isWithoutBreak', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('day', models.CharField(max_length=10, choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday')])),
                ('time_from', models.CharField(max_length=50, null=True)),
                ('time_to', models.CharField(max_length=50, null=True)),
                ('isDayOff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='branch',
            name='branchBreak',
            field=models.ForeignKey(related_name='branches', to='branchesInfo.Break'),
        ),
        migrations.AddField(
            model_name='branch',
            name='currencies',
            field=models.ManyToManyField(related_name='branches', to='branchesInfo.Currency'),
        ),
        migrations.AddField(
            model_name='branch',
            name='schedule',
            field=models.ManyToManyField(related_name='branches', to='branchesInfo.Schedule'),
        ),
        migrations.AddField(
            model_name='branch',
            name='services',
            field=models.ManyToManyField(related_name='branches', to='branchesInfo.Service'),
        ),
    ]
