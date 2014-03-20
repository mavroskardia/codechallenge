from hashlib import md5

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class Coder(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=256, blank=True)
	tagline = models.CharField(max_length=1024, blank=True)
	about = models.TextField(blank=True)
	xp = models.BigIntegerField(default=0)

	def level(self):
		return Level.objects.filter(starting_xp__lte=self.xp).order_by('-starting_xp').first()

	def webname(self):
		return self.name or self.user.username

	def avatar_url(self):
		h = md5(self.user.email.strip().lower().encode()).hexdigest()
		return 'http://www.gravatar.com/avatar/%s.jpg' % h

	def __str__(self):
		return self.__unicode__()

	def __unicode__(self):
		return '{name} ({self.xp})'.format(name=self.webname(), self=self)

class Level(models.Model):
	name = models.CharField(max_length=256)
	starting_xp = models.BigIntegerField()

	def __str__(self):
		return self.__unicode__()

	def __unicode__(self):
		return '{self.name} ({self.starting_xp})'.format(self=self)


# add signals for Coder here