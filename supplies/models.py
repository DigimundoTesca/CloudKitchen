# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator

class Provider(models.Model):
	name  = models.CharField(max_length = 255, unique = True)
	image = models.ImageField(blank = False)	

	def __str__(self):
		return self.name

	class Meta:
		ordering            = ('id',)
		verbose_name        = 'Provider'
		verbose_name_plural = 'Providers'
		

class Category(models.Model):
	name  = models.CharField(max_length = 255, unique = True)
	image = models.ImageField(blank = False)	

	def __str__(self):
		return self.name

	class Meta:
		ordering            = ('id',)
		verbose_name        = 'Category'
		verbose_name_plural = 'Categories'


class Supply(models.Model):
	name     = models.CharField(max_length = 255, unique = True)
	category = models.ForeignKey(Category, default = 1)
	barcode  = models.PositiveIntegerField(help_text='(Codigo de barras de 13 digitos)', validators=[MaxValueValidator(9999999999999)], blank = True, null = True)
	provider = models.ForeignKey(Provider, default = 1)
	image    = models.ImageField(blank = False)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ('id',)
		verbose_name        = 'Supply'
		verbose_name_plural = 'Supplies'