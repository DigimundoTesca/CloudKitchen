from django.db import models

from branchoffices.models import Supplier
from products.models import Supply
from users.models import User as UserProfile


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
