# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-07 23:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0020_remove_addresults_fixture_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addresults',
            name='tournment_id',
        ),
        migrations.AddField(
            model_name='addresults',
            name='fixture_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Manager.AddFixture'),
            preserve_default=False,
        ),
    ]
