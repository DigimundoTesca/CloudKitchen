# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplies', '0047_auto_20161031_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='waste',
            field=models.FloatField(default=0),
        ),
    ]