from django.db import models

from branchoffices.models import CashRegister
from products.models import Cartridge, PackageCartridge
from users.models import User as UserProfile


class Ticket(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(UserProfile, default=1, on_delete=models.CASCADE)
    cash_register = models.ForeignKey(CashRegister, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('-created_at',)
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

