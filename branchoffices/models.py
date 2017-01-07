from django.core.validators import MinLengthValidator
from django.db import models

from users.models import Profile


class BranchOffice(models.Model):
    name = models.CharField(max_length=90, default='')
    address = models.CharField(max_length=255, default='')
    manager = models.ForeignKey(Profile, on_delete=models.CASCADE)

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