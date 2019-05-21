# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-16 02:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0022_auto_20190511_2016'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddGoalsandAssist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Scorer_name', models.CharField(max_length=20)),
                ('assist_name', models.CharField(max_length=20)),
                ('g_time', models.CharField(max_length=20)),
                ('matchname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.AddFixture_table')),
                ('team_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.AddTeam')),
                ('tour_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.AddTournments')),
            ],
        ),
    ]
