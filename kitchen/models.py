from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from products.models import Supply, Cartridge, PackageCartridge
from sales.models import Ticket, TicketDetail


class ProcessedProduct(models.Model):
    # Status
    PENDING = 'PE'
    ASSEMBLED = 'AS'

    STATUS = (
        (PENDING, 'Pendiente'),
        (ASSEMBLED, 'Ensamblado'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    prepared_at = models.DateTimeField(editable=True, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default=ASSEMBLED)
    ticket_detail = models.OneToOneField(TicketDetail, on_delete=models.CASCADE)
    cartridge_parent = models.ForeignKey(Cartridge, null=True, blank=True)
    package_parent = models.ForeignKey(PackageCartridge, null=True, blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return '%s' % self.created_at

    @receiver(post_save, sender=TicketDetail)
    def create_processed_product(sender, instance, **kwargs):
        ticket_detail = TicketDetail.objects.get(id=instance.id)
        status = 'PE'
        quantity = instance.quantity

        def get_cartridge():
            if instance.cartridge:
                return instance.cartridge
            return None

        def get_package_cartridge():
            if instance.package_cartridge:
                return instance.package_cartridge
            return None

        processed_product = ProcessedProduct.objects.create(
            ticket_detail=ticket_detail,
            status=status,
            cartridge_parent=get_cartridge(),
            package_parent=get_package_cartridge(),
            quantity=quantity,
        )
        processed_product.save()

    class Meta:
        ordering = ('id',)
        verbose_name = 'Productos'
        verbose_name_plural = 'Productos Procesados'


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

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Insumo en Almacén'
        verbose_name_plural = 'Insumos en el Almacén'
