# -*- encoding: utf-8 -*-
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


class BranchOffice(models.Model):
    name = models.CharField(max_length=90, default='')
    address = models.CharField(max_length=255, default='')
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
    branch_office = models.ForeignKey(BranchOffice, default=1, on_delete=models.CASCADE)
    code = models.CharField(max_length=9, default='Cash_')

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Cash Register'
        verbose_name_plural = 'Cash Registers'


class Provider(models.Model):
    name = models.CharField(validators=[MinLengthValidator(4)], max_length=255, unique=True)
    image = models.ImageField(blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'


class Category(models.Model):
    name = models.CharField(validators=[MinLengthValidator(4)], max_length=125, unique=True)
    image = models.ImageField(blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class SupplyLocation(models.Model):
    location = models.CharField(max_length=90, default='')
    branch_office = models.ForeignKey(BranchOffice, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.location

    class Meta:
        ordering = ('id',)
        verbose_name = 'Supplies Location'
        verbose_name_plural = 'Supplies Locations'


class Supply(models.Model):
    DRY_ENVIRONMENT = 'DR'
    REFRIGERATION = 'RE'
    FREEZING = 'FR'

    DAYS = 'DA'
    MONTHS = 'MO'
    YEARS = 'YE'

    REQUIREMENTS = (
        (DRY_ENVIRONMENT, 'Ambiente Seco'),
        (REFRIGERATION, 'Refrigeración'),
        (FREEZING, 'Congelación'),
    )

    OPTIMAL_DURATION = (
        (DAYS, 'Dias'),
        (MONTHS, 'Meses'),
        (YEARS, 'Años'),
    )

    name = models.CharField(validators=[MinLengthValidator(4)], max_length=125, unique=True)
    category = models.ForeignKey(Category, default=1, on_delete=models.CASCADE)
    barcode = models.PositiveIntegerField(
        help_text='(Código de barras de 13 dígitos)',
        validators=[MaxValueValidator(9999999999999)], blank=True, null=True)
    provider = models.ForeignKey(Provider, default=1, on_delete=models.CASCADE)
    requirement = models.CharField(choices=REQUIREMENTS, default=DRY_ENVIRONMENT, max_length=2)
    base_cost = models.FloatField(default=0)
    optimal_duration = models.IntegerField(default=10)
    optimal_duration_unit = models.CharField(choices=OPTIMAL_DURATION, max_length=2, default=DAYS)
    location = models.ForeignKey(SupplyLocation, default=1)
    created_at = models.DateTimeField(editable=False, auto_now=True)
    image = models.ImageField(blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Supply'
        verbose_name_plural = 'Supplies'


class Order(models.Model):
    CANCELED = 'CA'
    IN_PROCESS = 'IP'
    RECEIVED = 'RE'
    STATUS = (
        (IN_PROCESS, 'Pedido'),
        (RECEIVED, 'Recibido'),
        (CANCELED, 'Cancelado'),
    )

    status = models.CharField(choices=STATUS, default=IN_PROCESS, max_length=2)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrdersDetails(models.Model):
    order = models.ForeignKey(Order, default=1, on_delete=models.CASCADE)
    supply = models.ForeignKey(Supply, default=1, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    metric = models.CharField(choices=METRICS, default=BOX, max_length=2)
    cost = models.FloatField(default=1)

    def __str__(self):
        return '%s %s %s' % (self.id, self.supply, self.quantity)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Order Details'
        verbose_name_plural = 'Orders Details'


class Cartridge(models.Model):
    FOOD_DISHES = 'FD'
    DRINKS = 'DR'

    CATEGORIES = (
        (FOOD_DISHES, 'Platillos'),
        (DRINKS, 'Bebidas'),
    )

    name = models.CharField(max_length=128, default='')
    category = models.CharField(choices=CATEGORIES, default=FOOD_DISHES, max_length=2)
    created_at = models.DateTimeField(editable=False, auto_now=True, auto_now_add=False)
    price = models.FloatField(default=1)
    supplies = models.ManyToManyField(Supply, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Cartridge'
        verbose_name_plural = 'Cartridges'


class PackageCartridges(models.Model):
    name = models.CharField(max_length=90)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    cartridges = models.ManyToManyField(Cartridge, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Package Cartridges'
        verbose_name_plural = 'Packages Cartridges'


class Warehouse(models.Model):
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

    supply = models.ForeignKey(Supply, default=1, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, default=PROVIDER, max_length=15)
    created_at = models.DateField(editable=False, auto_now_add=True)
    expiry_date = models.DateField(editable=True, auto_now_add=True)
    quantity = models.FloatField(default=0)
    waste = models.FloatField(default=0)
    cost = models.FloatField(default=0)
    cartridge_id = models.ForeignKey(Cartridge, blank=True, null=True, on_delete=models.CASCADE, default=1)
    parent_order = models.ForeignKey(Order, default=1)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouse'


class Ticket(models.Model):
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    cash_register = models.ForeignKey(CashRegister, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ticket Details'
        verbose_name_plural = 'Tickets Details'


class TicketDetails(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    cartridge = models.ForeignKey(Cartridge, default=1, on_delete=models.CASCADE)
    package_cartridges = models.ForeignKey(PackageCartridges, on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ticket Details'
        verbose_name_plural = 'Tickets Details'
