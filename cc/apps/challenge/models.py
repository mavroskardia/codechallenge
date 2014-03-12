import datetime

from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models


class Challenge(models.Model):
	name = models.CharField(max_length=256)
	duration = models.IntegerField(verbose_name="Duration (days)")

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.__unicode__()

	def owner(self):
		return self.participant_set.get(is_owner=True)

class Rule(models.Model):
	description = models.TextField()
	challenge = models.ForeignKey(Challenge)

	def __unicode__(self):
		return self.description[0:20]

	def __str__(self):
		return self.__unicode__()

class Participant(models.Model):
	'''The joining of a coder to a challenge and the fields that apply specifically to the pair'''

	coder = models.ForeignKey('coder.Coder')
	challenge = models.ForeignKey(Challenge)
	is_owner = models.BooleanField(default=False)
	date_joined = models.DateTimeField(default=lambda:timezone.now())

	class Meta:
		unique_together = ('coder', 'challenge',)

	def end_date(self):
		return datetime.timedelta(days=self.challenge.duration) + self.date_joined

	def days_left(self):
		elapsed = timezone.now() - self.date_joined
		return self.challenge.duration - elapsed.days

	def percent_complete(self):
		now = timezone.now()
		end = self.end_date()

		return (end - now).total_seconds() / (end - self.date_joined).total_seconds() * 100

	def clean(self, *args, **kwargs):
		error_txt = 'There can only be one owner per Challenge'

		owners = self.challenge.participant_set.filter(is_owner=True)

		# if there are owners and it's not this participant, bail:
		if len(owners) > 0 and self.is_owner and self != owners[0]:
			raise ValidationError(error_txt)

		super(Participant, self).clean(*args, **kwargs)

	def __unicode__(self):
		return '%s + %s' % (self.coder, self.challenge)

	def __str__(self):
		return self.__unicode__()

