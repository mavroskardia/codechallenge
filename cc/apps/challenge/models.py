from django.db import models


class Challenge(models.Model):
	name = models.CharField(max_length=256)
	duration = models.IntegerField(verbose_name="Duration (days)")

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.__unicode__()

class Rule(models.Model):
	description = models.TextField()
	challenge = models.ForeignKey('challenge.Challenge')

	def __unicode__(self):
		return self.description[0:20]

	def __str__(self):
		return self.__unicode__()