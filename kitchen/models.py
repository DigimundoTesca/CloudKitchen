from django.db import models

from products.models import Supply, Cartridge, PackageCartridge


class ProcessedCartridge(models.Model):
    # Status
    ASSEMBLED = 'AS'
    SOLD = 'SE'
    DELIVERED = 'DE'

    STATUS = (
        (ASSEMBLED, 'Ensamblado'),
        (SOLD, 'Vendido'),
        (DELIVERED, 'Entregado'),
    )
    created_at = models.DateTimeField(editable=False, auto_now=True, auto_now_add=False)
    status = models.CharField(max_length=10, choices=STATUS, default=ASSEMBLED)
    supplies = models.ManyToManyField(Supply, blank=True)
    cartridge_parent = models.ForeignKey(Cartridge, default=1, on_delete=models.CASCADE)
    package_cartridge_parent = models.ForeignKey(PackageCartridge, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Cartuchos'
        verbose_name_plural = 'Cartuchos Procesados'


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
        verbose_name = 'Insumo en Almacén'
        verbose_name_plural = 'Insumos en el Almacén'
