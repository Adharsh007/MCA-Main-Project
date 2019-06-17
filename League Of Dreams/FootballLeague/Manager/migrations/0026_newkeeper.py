# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-06-13 00:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0025_auto_20190517_0926'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewKeeper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saves', models.IntegerField()),
                ('gk_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.AddPlayer')),
                ('matchname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.AddFixture_table')),
                ('team_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.AddTeam')),
                ('tour_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.AddTournments')),
            ],
        ),
    ]
