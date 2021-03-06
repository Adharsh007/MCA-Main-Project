# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-16 06:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0023_addgoalsandassist'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddGoalKeeperSaves',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gk_names', models.CharField(max_length=20)),
                ('saves', models.IntegerField()),
                ('matchname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.AddFixture_table')),
                ('team_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.AddTeam')),
                ('tour_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.AddTournments')),
            ],
        ),
    ]
