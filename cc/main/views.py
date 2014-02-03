from django.http import HttpResponse
from django.shortcuts import render


def home(req):
	return render(req, 'main/home.html', {})
