# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-10 05:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0019_auto_20190509_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addpoints',
            name='tourn_name_id',
            field=models.IntegerField(),
        ),
    ]