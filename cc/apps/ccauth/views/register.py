from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse

from apps.ccauth.forms import RegistrationForm
from apps.coder.models import Coder


class RegisterView(View):
    form_class = RegistrationForm
    template_name = 'ccauth/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, { 'form': form })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')

            user = User.objects.create_user(username, email, password)
            coder = Coder()
            coder.user = user
            coder.save()

            logout(request)
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.info(request, 'Successfully registered as a coder! Please take a moment to fill out your profile.')

            return HttpResponseRedirect(reverse('coder:profile', args=(user.username,)))

        return render(request, self.template_name, { 'form': form })
