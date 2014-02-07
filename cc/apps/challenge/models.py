from django.db import models


class Challenge(models.Model):
	name = models.CharField(max_length=256)
	rules = models.TextField()
	duration = models.IntegerField(verbose_name="Duration (days)")
	start = models.DateField()
	end = models.DateField()
	#participants = models.OneToMany('coder.Coder') guess we don't need this since we could use coder_set
