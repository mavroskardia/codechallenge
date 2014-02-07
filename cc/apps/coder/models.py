from django.db import models
from django.contrib.auth.models import User

class Coder(models.Model):
	user = models.OneToOneField(User)
	name = models.CharField(max_length=256, blank=True)
	tagline = models.CharField(max_length=1024, blank=True)
	about = models.TextField(blank=True)
	xp = models.BigIntegerField(default=0)
	level = models.ForeignKey('Level', null=True)
	challenges = models.ManyToManyField('challenge.Challenge')

class Level(models.Model):
	name = models.CharField(max_length=256)
	starting_xp = models.BigIntegerField()
