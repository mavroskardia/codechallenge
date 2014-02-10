from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.forms import AuthenticationForm


class IndexView(View):
	template_name = 'ccauth/index.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)
