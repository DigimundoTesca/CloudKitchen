# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


class Provider(models.Model):
    name  = models.CharField(validators=[MinLengthValidator(4)], max_length=255, unique=True)
    image = models.ImageField(blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'


class Category(models.Model):
    name  = models.CharField(validators=[MinLengthValidator(4)], max_length=125, unique=True)
    image = models.ImageField(blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Supply(models.Model):
    name             = models.CharField(validators=[MinLengthValidator(4)], max_length=125, unique=True)
    category         = models.ForeignKey(Category, default=1)
    barcode          = models.PositiveIntegerField(
        help_text='(Código de barras de 13 dígitos)',
        validators=[MaxValueValidator(9999999999999)], blank=True, null=True)
    provider         = models.ForeignKey(Provider, default=1)
    ideal_durability = models.IntegerField(default=10)
    image            = models.ImageField(blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Supply'
        verbose_name_plural = 'Supplies'


class Lot(models.Model):
    METRICS = (
        (1, 'empaques'),
        (2, 'cajas')
    )
    metric    = models.CharField(METRICS, max_length=10, default=1)
    parent_id = models.ForeignKey('self')

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Lot'
        verbose_name_plural = 'Lots'


class PackageCartridges(models.Model):
    name        = models.CharField(max_length=90)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Package Cartridges'
        verbose_name_plural = 'Packages Cartridges'


class Cartridge(models.Model):
    name                 = models.CharField(max_length=128 , default='')
    packageCartridges_id = models.ForeignKey(PackageCartridges, blank=True, null=True)
    created_at           = models.DateTimeField(editable=False, auto_now=True, auto_now_add=False)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Cartridge'
        verbose_name_plural = 'Cartridges'


class StockChain(models.Model):
    STATUS = (
        (1, 'Provider'),
        (2, 'Stock'),
        (3, 'Assembled'),
        (4, 'Selled')
    )
    METRICS = (
        (1, 'lt'),
        (2, 'gr')
    )

    supply        = models.ForeignKey(Supply, default=1)
    registered_at = models.DateField(editable=False, auto_now=True)
    expiry_date   = models.DateField()
    status        = models.CharField(max_length=1, choices=STATUS, default=1)
    metric        = models.CharField(METRICS, max_length=2, default=1)
    cartridge_id    = models.ForeignKey(Cartridge, blank=True, null=True)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Stock Chain'
        verbose_name_plural = 'Stocks Chain'


class CashRegisters(models.Model):
    STATUS = (
        (1, 'Active'),
        (2, 'Off')
    )
    status = models.CharField(max_length=10, default=STATUS)
