# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-27 06:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0012_addtournments'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournmentRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_registred', models.BooleanField(default=False)),
                ('team_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.AddTeam')),
                ('tr_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.AddTournments')),
            ],
        ),
    ]
