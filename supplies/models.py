# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator
from django.db import models


class UserRol(models.Model):
    rol = models.CharField(max_length=90, default='')
    
    def __str__(self):
        return self.rol
    
    class Meta:
        verbose_name = 'User Rol'
        verbose_name_plural = 'User Roles'
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    phone_number = models.PositiveIntegerField(
        help_text='(Número telefónico a 10 dígitos)',
        validators=[MaxValueValidator(9999999999)], blank=True, null=True)
    user_rol = models.ForeignKey(UserRol, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class BranchOffice(models.Model):
    name = models.CharField(max_length=90, default='')
    address = models.CharField(max_length=255, default='')
    manager = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

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
    code = models.CharField(max_length=9, default='Cash_')
    status = models.CharField(choices=STATUS, default=ACTIVE, max_length=10)
    branch_office = models.ForeignKey(BranchOffice, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Cash Register'
        verbose_name_plural = 'Cash Registers'


class Supplier(models.Model):
    name = models.CharField(validators=[MinLengthValidator(4)], max_length=255, unique=True)
    image = models.ImageField(blank=False, upload_to='media/suppliers')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'


class SuppliesCategory(models.Model):
    name = models.CharField(validators=[MinLengthValidator(4)], max_length=125, unique=True)
    image = models.ImageField(blank=False, upload_to='media/supplies-categories')

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
    # storage requirement
    DRY_ENVIRONMENT = 'DR'
    REFRIGERATION = 'RE'
    FREEZING = 'FR'
    STORAGE_REQUIREMENTS = (
        (DRY_ENVIRONMENT, 'Ambiente Seco'),
        (REFRIGERATION, 'Refrigeración'),
        (FREEZING, 'Congelación'),
    )

    # optimal duration
    DAYS = 'DA'
    MONTHS = 'MO'
    YEARS = 'YE'
    OPTIMAL_DURATION = (
        (DAYS, 'Dias'),
        (MONTHS, 'Meses'),
        (YEARS, 'Años'),
    )

    # presentation unit
    PACKAGE = 'PA'
    BOX = 'BO'
    PIECE = 'PI'
    PRESENTATION_UNIT = (
        (PACKAGE, 'Paquete'),
        (BOX, 'Caja'),
        (PIECE, 'Pieza')
    )

    # metrics
    GRAM = 'GR'
    LITER = 'LI'
    PIECE = 'PI'

    METRICS = (
        (GRAM, 'gramo'),
        (LITER, 'mililitro'),
        (PIECE, 'pieza'),
    )

    name = models.CharField(validators=[MinLengthValidator(2)], max_length=125, unique=True)
    category = models.ForeignKey(SuppliesCategory, default=1, on_delete=models.CASCADE)
    barcode = models.PositiveIntegerField(
        help_text='(Código de barras de 13 dígitos)',
        validators=[MaxValueValidator(9999999999999)], blank=True, null=True)
    supplier = models.ForeignKey(Supplier, default=1, on_delete=models.CASCADE)
    storage_required = models.CharField(choices=STORAGE_REQUIREMENTS, default=DRY_ENVIRONMENT, max_length=2)
    presentation_unit = models.CharField(max_length=10, choices=PRESENTATION_UNIT, default=PACKAGE)
    presentation_cost = models.FloatField(default=0)
    measurement_quantity = models.FloatField(default=0)
    measurement_unit = models.CharField(max_length=10, choices=METRICS, default=PACKAGE)
    optimal_duration = models.IntegerField(default=0)
    optimal_duration_unit = models.CharField(choices=OPTIMAL_DURATION, max_length=2, default=DAYS)
    location = models.ForeignKey(SupplyLocation, default=1, on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False, auto_now=True)
    image = models.ImageField(blank=False, upload_to='media/supplies')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Supply'
        verbose_name_plural = 'Supplies'


class SupplierOrder(models.Model):
    CANCELED = 'CA'
    IN_PROCESS = 'IP'
    RECEIVED = 'RE'
    STATUS = (
        (IN_PROCESS, 'Pedido'),
        (RECEIVED, 'Recibido'),
        (CANCELED, 'Cancelado'),
    )

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    status = models.CharField(choices=STATUS, default=IN_PROCESS, max_length=2)
    user_charge = models.ForeignKey(UserProfile, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class SupplierOrderDetail(models.Model):
    order = models.ForeignKey(SupplierOrder, default=1, on_delete=models.CASCADE)
    supply = models.ForeignKey(Supply, default=1, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cost = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    supplier = models.ForeignKey(Supplier, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (self.id, self.supply, self.quantity)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Supplier Order Details'
        verbose_name_plural = 'Supplier Orders Details'


class Cartridge(models.Model):
    # Categories
    FOOD_DISHES = 'FD'
    DRINKS = 'DR'

    CATEGORIES = (
        (FOOD_DISHES, 'Platillos'),
        (DRINKS, 'Bebidas'),
    )

    name = models.CharField(max_length=128, default='')
    price = models.DecimalField(decimal_places=2, default=0, max_digits=12)
    category = models.CharField(choices=CATEGORIES, default=FOOD_DISHES, max_length=2)
    created_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=False, upload_to='media/cartridges')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Cartridge'
        verbose_name_plural = 'Cartridges'


class CartridgeRecipe(models.Model):
    cartridge = models.ForeignKey(Cartridge, default=1, on_delete=models.CASCADE)
    supply = models.ForeignKey(Supply, default=1, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return '%s' % self.cartridge

    class Meta:
        ordering = ('id',)
        verbose_name = 'Cartridge Recipe'
        verbose_name_plural = 'Cartridges Recipes'


class PackageCartridge(models.Model):
    name = models.CharField(max_length=90)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    package_active = models.BooleanField(default=False)
    image = models.ImageField(blank=True, upload_to='media/package-cartridges')
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Package Cartridges'
        verbose_name_plural = 'Packages Cartridges'


class PackageCartridgeRecipe(models.Model):
    package_cartridge = models.ForeignKey(PackageCartridge, default=1, on_delete=models.CASCADE)
    cartridge = models.ForeignKey(Cartridge, default=1, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return '%s' % self.package_cartridge

    class Meta:
        ordering = ('id',)
        verbose_name = 'Package Cartridge Recipe'
        verbose_name_plural = 'Package Cartridges Recipes'


class ProcessedCartridge(models.Model):
    # Status
    ASSEMBLED = 'AS'
    SOLD = 'SE'

    STATUS = (
        (ASSEMBLED, 'Ensamblado'),
        (SOLD, 'Vendido')
    )
    name = models.CharField(Supply, max_length=125)
    created_at = models.DateTimeField(editable=False, auto_now=True, auto_now_add=False)
    status = models.CharField(max_length=10, choices=STATUS, default=ASSEMBLED)
    supplies = models.ManyToManyField(Supply, blank=True)
    cartridge_parent = models.ForeignKey(Cartridge, default=1, on_delete=models.CASCADE)
    package_cartridge_parent = models.ForeignKey(PackageCartridge, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Processed Cartridge'
        verbose_name_plural = 'Processed Cartridges'


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
    processed_cartridge = models.ForeignKey(ProcessedCartridge, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouse'


class Ticket(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(UserProfile, default=1, on_delete=models.CASCADE)
    cash_register = models.ForeignKey(CashRegister, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Ticket '
        verbose_name_plural = 'Tickets'


class TicketDetail(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    cartridge = models.ForeignKey(Cartridge, on_delete=models.CASCADE, blank=True, null=True)
    package_cartridge = models.ForeignKey(PackageCartridge, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.FloatField(default=0)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ticket Details'
        verbose_name_plural = 'Tickets Details'


class CustomerOrder(models.Model):
    IN_PROCESS = 'PR'
    SOLD = 'SO'
    CANCELLED = 'CA'

    STATUS = (
        (IN_PROCESS, 'En proceso',),
        (SOLD, 'Vendido'),
        (CANCELLED, 'Cancelado'),
    )
    customer_user = models.ForeignKey(UserProfile, default=1)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    delivery_date = models.DateTimeField(auto_created=True, editable=True)
    status = models.CharField(max_length=10, choices=STATUS, default=IN_PROCESS)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    score = models.PositiveIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        null=False, blank=False, default=1)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Customer Order'
        verbose_name_plural = 'Customer Orders'


class CustomerOrderDetail(models.Model):
    IN_PROCESS = 'PR'
    SOLD = 'SE'
    CANCELLED = 'CA'

    STATUS = (
        (IN_PROCESS, 'En proceso',),
        (SOLD, 'Vendido'),
        (CANCELLED, 'Cancelado'),
    )
    customer_order = models.ForeignKey(CustomerOrder, default=1, on_delete=models.CASCADE)
    cartridge = models.ForeignKey(Cartridge, on_delete=models.CASCADE, blank=True, null=True)
    package_cartridge = models.ForeignKey(PackageCartridge, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Customer Order Detail'
        verbose_name_plural = 'Customer Order Details'
