from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from supplies.models import Cartridge, PackageCartridge
from users.models import UserProfile


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
    pin = models.CharField(default='1234', max_length=254, blank=False)

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
