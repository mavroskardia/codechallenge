from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib import messages
from django.core.urlresolvers import reverse

from apps.ccauth.forms import RegisterForm


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'ccauth/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, { 'form': form })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # do registration logic
            pass

        return render(request, self.template_name, { 'form': form })
