from django.db import models
from django.db.models import Avg, Sum
from django.utils import timezone

from branchoffices.models import CashRegister
from products.models import Cartridge, PackageCartridge
from users.models import User as UserProfile

class TicketBase(models.Model):
    # Payment Type
    CASH = 'CA'
    CREDIT = 'CR'

    PAYMENT_TYPE = (
        (CASH, 'Efectivo'),
        (CREDIT, 'Crédito'),
    )

    order_number = models.IntegerField(default=1)
    created_at = models.DateTimeField(editable=True)
    payment_type = models.CharField(
        choices=PAYMENT_TYPE, default=CASH, max_length=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.id

    def save(self, *args, **kwargs):
        """ On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        return super(TicketBase, self).save(*args, **kwargs)

    def total(self):
        cartridge_tickets_details = CartridgeTicketDetail.objects.filter(ticket_base=self.id)
        package_tickets_details = PackageCartridgeTicketDetail.objects.filter(ticket_base=self.id)
        total = 0

        for c in cartridge_tickets_details:
            total += c.price

        for p in package_tickets_details:
            total += p.price
        return total

    def ticket_details(self):
        cartridge_tickets_details = CartridgeTicketDetail.objects.filter(ticket_base=self.id)
        package_tickets_details = PackageCartridgeTicketDetail.objects.filter(ticket_base=self.id)
        options = []

        for cartridge_ticket_detail in cartridge_tickets_details:
                options.append(("<option value=%s selected>%s</option>" %
                                (cartridge_ticket_detail, cartridge_ticket_detail.cartridge)))

        for package_ticket_detail in package_tickets_details:
                options.append(("<option value=%s selected>%s</option>" %
                                (package_ticket_detail, package_ticket_detail.package_cartridge)))

        return """<select multiple>%s</select>""" % str(options)

    ticket_details.allow_tags = True

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Ticket Base'
        verbose_name_plural = 'Tickets Base'

class Ticket(models.Model):
    # Payment Type
    CASH = 'CA'
    CREDIT = 'CR'

    PAYMENT_TYPE = (
        (CASH, 'Efectivo'),
        (CREDIT, 'Crédito'),
    )

    created_at = models.DateTimeField(editable=True)
    seller = models.ForeignKey(
        UserProfile, default=1, on_delete=models.CASCADE)
    cash_register = models.ForeignKey(
        CashRegister, on_delete=models.CASCADE, default=1)
    payment_type = models.CharField(
        choices=PAYMENT_TYPE, default=CASH, max_length=2)
    order_number = models.IntegerField(
        null=True)

    def __str__(self):
        return '%s' % self.id

    def save(self, *args, **kwargs):
        """ On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        return super(Ticket, self).save(*args, **kwargs)

    def total(self):
        tickets_details = TicketDetail.objects.filter(ticket=self.id)
        total = 0
        for x in tickets_details:
            total += x.price
        return total

    def ticket_details(self):
        tickets_details = TicketDetail.objects.filter(ticket=self.id)
        options = []

        for ticket_detail in tickets_details:
            if ticket_detail.cartridge:
                options.append(("<option value=%s>%s</option>" %
                                (ticket_detail, ticket_detail.cartridge)))
            elif ticket_detail.package_cartridge:
                options.append(("<option value=%s>%s</option>" %
                                (ticket_detail, ticket_detail.package_cartridge)))
        tag = """<select>%s</select>""" % str(options)
        return tag

    ticket_details.allow_tags = True

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Ticket '
        verbose_name_plural = 'Tickets'


class TicketDetail(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    cartridge = models.ForeignKey(
        Cartridge, on_delete=models.CASCADE, blank=True, null=True)
    package_cartridge = models.ForeignKey(
        PackageCartridge, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def created_at(self):
        return self.ticket.created_at

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ticket Details'
        verbose_name_plural = 'Tickets Details'


class CartridgeTicketDetail(models.Model):
    cartridge = models.ForeignKey(Cartridge, on_delete=models.CASCADE)
    ticket_base = models.ForeignKey(TicketBase, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle del Ticket para Cartuchos'
        verbose_name_plural = 'Detalles de Tickets para Cartuchos'

    def __str__(self):
        return '%s' % self.ticket_base

class PackageCartridgeTicketDetail(models.Model):
    ticket_base = models.ForeignKey(TicketBase, on_delete=models.CASCADE)
    package_cartridge = models.ForeignKey(PackageCartridge, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle del Ticket para Paquetes'
        verbose_name_plural = 'Detalles de Tickets para Paquetes'

    def __str__(self):
        return '%s' % self.ticket_base
        