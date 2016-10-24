# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator
GRAM = 'GR'
LITER = 'LI'
PIECE = 'PI'
PACKAGE = 'PA'
BOX = 'BO'

METRICS = (
    (GRAM, 'gramo'),
    (LITER, 'litro'),
    (PIECE, 'pieza'),
    (PACKAGE, 'paquete'),
    (BOX, 'caja')
)

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


class Order(models.Model):
    CANCELED   = 'CA'
    IN_PROCESS = 'IP'
    RECEIVED   = 'RE'
    STATUS = (
        (IN_PROCESS, 'En proceso'),
        (RECEIVED, 'Recibido'),
        (CANCELED, 'Cancelado'),
    )
    created_at       = models.DateTimeField(editable=False, auto_now=True, auto_now_add=False)
    last_modified_at = models.DateTimeField(editable=False, auto_now=True, auto_now_add=False)
    status           = models.CharField(choices=STATUS, default=IN_PROCESS, max_length=2)

    def __str__(self):
        date_time = ('%s' % self.last_modified_at)

        return '%s' % date_time

    class Meta:
        ordering = ('id',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class OrdersDetails(models.Model):
    order    = models.ForeignKey(Order, default=1)
    supply   = models.ForeignKey(Supply, default=1)
    quantity = models.PositiveIntegerField(default=1)
    metric   = models.CharField(choices=METRICS, default=BOX, max_length=2)
    cost     = models.FloatField(default=1)

    def __str__(self):
        return '%s %s %s' % (self.id, self.supply, self.quantity)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Order Details'
        verbose_name_plural = 'Orders Details'


class Lot(models.Model):
    metric    = models.CharField(choices=METRICS, max_length=10, default=PACKAGE)
    parent_id = models.ForeignKey('self')

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Lot'
        verbose_name_plural = 'Lots'


class PackageCartridges(models.Model):
    name  = models.CharField(max_length=90)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Package Cartridges'
        verbose_name_plural = 'Packages Cartridges'


class Cartridge(models.Model):
    name                 = models.CharField(max_length=128, default='')
    packageCartridges    = models.ManyToManyField(PackageCartridges)
    created_at           = models.DateTimeField(editable=False, auto_now=True, auto_now_add=False)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Cartridge'
        verbose_name_plural = 'Cartridges'


class StockChain(models.Model):
    PROVIDER = 'PR'
    STOCK = 'ST'
    ASSEMBLED = 'AS'
    SOLD = 'SO'
    STATUS = (
        (PROVIDER, 'Provider'),
        (STOCK, 'Stock'),
        (ASSEMBLED, 'Assembled'),
        (SOLD, 'Sold'),
    )

    supply        = models.ForeignKey(Supply, default=1)
    registered_at = models.DateField(editable=False, auto_now=True)
    expiry_date   = models.DateField()
    status        = models.CharField(choices=STATUS, default=PROVIDER, max_length=15)
    metric        = models.CharField(choices=METRICS, default=GRAM, max_length=10)
    cartridge_id    = models.ForeignKey(Cartridge, blank=True, null=True)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Stock Chain'
        verbose_name_plural = 'Stocks Chain'


class BranchOffice(models.Model):
    name    = models.CharField(max_length=90, default='')
    addres  = models.CharField(max_length=255, default='')
    manager = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Branch Office'
        verbose_name_plural = 'Branch Offices'


class CashRegister(models.Model):
    ACTIVE = 'AC'
    OFF = 'OF'
    STATUS = (
        (ACTIVE, 'On'),
        (OFF, 'Off'),
    )
    status = models.CharField(choices=STATUS, default=ACTIVE, max_length=10)
    branch_office = models.ForeignKey(BranchOffice, default=1)
    code = models.CharField(max_length=5, default='Dab')

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Cash Register'
        verbose_name_plural = 'Cash Registers'