from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages

from apps.challenge.models import Challenge
from apps.coder.models import Coder


def home(request):
	return render(request, 'landing/home.html', {
		'recent_challenges': Challenge.objects.order_by('-id')[:5]
		})