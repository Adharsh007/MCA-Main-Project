# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-10 05:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0020_auto_20190509_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addpoints',
            name='tourn_name_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.AddTournments'),
        ),
    ]
