from __future__ import unicode_literals

from django.db import models

class User(models.Model):
	name   = models.CharField(max_length = 255)
	avatar = models.ImageField(blank = False)	

	def __str__(self):
		return self.name

	class Meta:
		ordering            = ('id',)
		verbose_name        = 'User'
		verbose_name_plural = 'Users'
