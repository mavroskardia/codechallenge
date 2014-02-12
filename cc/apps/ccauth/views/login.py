from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib import messages
from django.core.urlresolvers import reverse

from apps.ccauth.forms import LoginForm


class LoginView(View):
    form_class = LoginForm
    template_name = 'ccauth/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        next = request.GET.get('next') or '/'
        return render(request, self.template_name, { 'form': form, 'next': next })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    
                    if 'next' in request.POST:
                        return HttpResponseRedirect(request.POST['next'])

                    return HttpResponseRedirect(reverse('home'))
                else:
                    messages.error(request, 'Not an active user')
            else:
                messages.error(request, 'Invalid username or password')

        return render(request, self.template_name, { 'form': form })
