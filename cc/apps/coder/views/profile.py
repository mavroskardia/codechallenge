from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib import messages
from django.core.urlresolvers import reverse

from ..models import Coder
from ..forms import ProfileForm


class ProfileView(View):
    form_class = ProfileForm
    ro_template_name = 'coder/ro_profile.html'
    rw_template_name = 'coder/rw_profile.html'

    def get(self, request, username, *args, **kwargs):
        coder = get_object_or_404(Coder, user__username=username)

        if request.user == coder.user:
            return render(request, self.rw_template_name, { 'coder': coder, 'form': self.form_class() })

        return render(request, self.ro_template_name, { 'coder': coder })

    def post(self, request, username, *args, **kwargs):
        coder = get_object_or_404(Coder, user__username=username)

        form = self.form_class(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            tagline = form.cleaned_data.get('tagline')
            about = form.cleaned_data.get('about')

            if name: coder.name = name
            if tagline: coder.tagline = tagline
            if about: coder.about = about

            coder.save()

            messages.info(request, 'Successfully updated profile')

        return render(request, self.rw_template_name, { 'coder': coder, 'form': form })