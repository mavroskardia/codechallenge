from django.http import HttpResponse
from django.shortcuts import render

from apps.challenge.models import Challenge
from apps.coder.models import Coder


def home(request):
	return render(request, 'landing/home.html', {
		'challenges': Challenge.objects.all()
		})