# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-06-23 23:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0027_livescore'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_one', models.CharField(max_length=20)),
                ('team_two', models.CharField(max_length=20)),
                ('team_1_goal', models.IntegerField()),
                ('team_2_goal', models.IntegerField()),
                ('m_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.AddFixture_table')),
                ('tourn_name_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.AddTournments')),
            ],
        ),
    ]
