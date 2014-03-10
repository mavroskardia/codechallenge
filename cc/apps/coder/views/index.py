from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.core.urlresolvers import reverse

from ..models import Coder

class IndexView(generic.ListView):
	model = Coder