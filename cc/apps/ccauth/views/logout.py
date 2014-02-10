from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib import auth
from django.contrib import messages
from django.core.urlresolvers import reverse


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.info(request, 'Successfully logged off.')
        return HttpResponseRedirect(reverse('home'))