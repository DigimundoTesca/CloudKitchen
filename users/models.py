# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.db import models
from django.contrib.auth.models import User as DjangoUser, AbstractUser
from django.utils import six


class Rol(models.Model):
    rol = models.CharField(max_length=90, default='')

    def __str__(self):
        return self.rol


class User(AbstractUser):
    phone_number = models.CharField(blank=True, null=True, max_length=10, default='', unique=True)
    user_rol = models.ForeignKey(Rol, blank=True, null=True)


class CustomerProfile(models.Model):
    # username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    # user_name = models.CharField(max_length=150, unique=True, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[username_validator], error_messages={ 'unique': 'Ya existe un usuario con ese nombre', }, )
    longitude = models.CharField(default='0.0', max_length=30, blank=True)
    latitude = models.CharField(default=0.0, max_length=30, blank=True)
    address = models.CharField(default='', max_length=255)
    first_dabba = models.BooleanField(default=False)
