# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator


class Provider(models.Model):
    name  = models.CharField(max_length=255, unique=True)
    image = models.ImageField(blank=False)    

    def __str__(self):
        return self.name

    class Meta:
        ordering            = ('id',)
        verbose_name        = 'Provider'
        verbose_name_plural = 'Providers'
        


class Category(models.Model):
    name  = models.CharField(max_length=125, unique=True)
    image = models.ImageField(blank = False)    

    def __str__(self):
        return self.name

    class Meta:
        ordering            = ('id',)
        verbose_name        = 'Category'
        verbose_name_plural = 'Categories'



class Supply(models.Model):
    name             = models.CharField(max_length=125, unique=True)
    category         = models.ForeignKey(Category, default=1)
    barcode          = models.PositiveIntegerField(
        help_text='(Codigo de barras de 13 digitos)', 
        validators=[MaxValueValidator(9999999999999)], 
        blank=True, 
        null=True)
    provider         = models.ForeignKey(Provider, default=1)
    ideal_durability = models.IntegerField(default=10)
    image            = models.ImageField(blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering            = ('id',)
        verbose_name        = 'Supply'
        verbose_name_plural = 'Supplies'



class Metric(models.Model):
    METRICS_TYPE = (
        ('gramos', 'gramos'),
        ('litros', 'litros'),
        ('empaques', 'empaques'),
        ('cajas', 'cajas')
    )
    metric_type   = models.CharField(max_length=8, choices=METRICS_TYPE)
    stock         = models.DecimalField(max_digits=9, decimal_places=3)
    parent_metric = models.ForeignKey('self', blank=True, null=True)

    def __str__(self):
        return '%s > %s > %s' % (self.stock, self.metric_type, self.parent_metric)

    class Meta:
        ordering            = ('id',)
        verbose_name        = 'Metric'
        verbose_name_plural = 'Metrics'


class PackageCartridges(models.Model):
    name        = models.CharField(max_length=90)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering            = ('name',)
        verbose_name        = 'Package Cartridges'
        verbose_name_plural = 'Packages Cartridges'


class Cartridge(models.Model):
    name                 = models.CharField(max_length=90)
    description          = models.CharField(max_length=255)
    packageCartridges_id = models.ForeignKey(PackageCartridges, blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering            = ('name',)
        verbose_name        = 'Cartridge'
        verbose_name_plural = 'Cartridges'


class StockChain(models.Model):
    STATUS = (
        ('1','Provider'),
        ('2','Stock'),
        ('3','Assemblied'),
        ('4','Selled')
    )
    registered_at = models.DateField()
    expiry_date   = models.DateField()
    supply        = models.ForeignKey(Supply, default=1)
    status        = models.CharField(max_length=1, choices=STATUS, default=1)
    metric        = models.ForeignKey(Metric, default = 1)
    cartridge_id  = models.ForeignKey(Cartridge, blank=True, null=True)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering            = ('id',)
        verbose_name        = 'Stock Chain'
        verbose_name_plural = 'Stocks Chain'

