# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Rol(models.Model):
    rol = models.CharField(max_length=90, default='')

    def __str__(self):
        return self.rol


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    phone_number = models.PositiveIntegerField(
        help_text='(Número telefónico a 10 dígitos)',
        validators=[MaxValueValidator(9999999999)], blank=True, null=True)
    user_rol = models.ForeignKey(Rol, blank=True, null=True)
    first_dabba = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class CustomerProfile(models.Model):
    username = models.CharField(default='', max_length=30, blank=False, unique=True)
    email = models.EmailField(max_length=255, blank=False, default='', unique=True)
    phone_number = models.CharField(blank=False, null=True, max_length=10, default='', unique=True)
    longitude = models.CharField(default='0.0', max_length=30, blank=True)
    latitude = models.CharField(default=0.0, max_length=30, blank=True)
    address = models.CharField(default='', max_length=255, blank=True)

    def __str__(self):
        return self.username
