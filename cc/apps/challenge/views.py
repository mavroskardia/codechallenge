from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Challenge

class IndexView(generic.ListView):
	model = Challenge

class DetailView(generic.DetailView):
	model = Challenge
