# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 20:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supplies', '0033_auto_20161027_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartridge',
            name='category',
            field=models.ForeignKey(default=1, max_length=2, on_delete=django.db.models.deletion.CASCADE, to='supplies.Category'),
        ),
    ]
