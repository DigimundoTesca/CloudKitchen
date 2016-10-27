# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 20:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supplies', '0034_auto_20161027_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartridge',
            name='category',
            field=models.ForeignKey(default=1, max_length=1, on_delete=django.db.models.deletion.CASCADE, to='supplies.Category'),
        ),
    ]