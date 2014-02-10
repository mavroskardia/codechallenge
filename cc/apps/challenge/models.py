from django.db import models


class Challenge(models.Model):
	name = models.CharField(max_length=256)
	rules = models.TextField()
	duration = models.IntegerField(verbose_name="Duration (days)")
	start = models.DateField()
	end = models.DateField()

class Rule(models.Model):
	description = models.TextField()
	challenge = models.ForeignKey('challenge.Challenge')