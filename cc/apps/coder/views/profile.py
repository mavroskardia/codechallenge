from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib import messages
from django.core.urlresolvers import reverse

from ..models import Coder


class ProfileView(View):
    ro_template_name = 'coder/ro_profile.html'
    rw_template_name = 'coder/rw_profile.html'

    def get(self, request, username, *args, **kwargs):
        coder = get_object_or_404(Coder, user__username=username)
        template = self.rw_template_name if request.user == coder.user else self.ro_template_name

        return render(request, template, { 'coder': coder })
