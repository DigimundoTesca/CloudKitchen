# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class CustomerProfile(models.Model):
    username = models.CharField(default='', max_length=30, blank=False, unique=True)
    email = models.EmailField(max_length=255, blank=False, default='', unique=True)
    phone_number = models.CharField(blank=False, null=True, max_length=10, default='', unique=True)
    longitude = models.CharField(default='0.0', max_length=30, blank=True)
    latitude = models.CharField(default=0.0, max_length=30, blank=True)
    address = models.CharField(default='', max_length=255, blank=True)

    def __str__(self):
        return self.username
