# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import six


class Rol(models.Model):
    rol = models.CharField(max_length=90, default='')

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.rol


class User(AbstractUser):
    phone_number = models.CharField(blank=True, null=True, max_length=10, default='', unique=True)
    user_rol = models.ForeignKey(Rol, blank=True, null=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    longitude = models.CharField(default='0.0', max_length=30, blank=True)
    latitude = models.CharField(default=0.0, max_length=30, blank=True)
    address = models.CharField(default='', max_length=255, blank=True, null=True)
    first_dabba = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            CustomerProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.customerprofile.save()