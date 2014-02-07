from django.db import models


class Coder(models.Model):
	name = models.CharField(max_length=256)
	tagline = models.CharField(max_length=1024)
	about = models.TextField()
	xp = models.BigIntegerField()
	level = models.ForeignKey('Level')
	challenges = models.ManyToManyField('challenge.Challenge')

class Level(models.Model):
	name = models.CharField(max_length=256)
	starting_xp = models.BigIntegerField()
