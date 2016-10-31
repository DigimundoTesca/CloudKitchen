# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-29 21:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplies', '0043_auto_20161028_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartridge',
            name='category',
            field=models.CharField(choices=[('FD', 'Platillos'), ('DR', 'Bebidas')], default='FD', max_length=2),
        ),
        migrations.AlterField(
            model_name='cartridge',
            name='packageCartridges',
            field=models.ManyToManyField(blank=True, to='supplies.PackageCartridges'),
        ),
        migrations.AlterField(
            model_name='supply',
            name='optimal_duration_unit',
            field=models.CharField(choices=[('DA', 'Dias'), ('MO', 'Meses'), ('YE', 'Años')], default='DA', max_length=2),
        ),
    ]
