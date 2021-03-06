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

    def get(self, request, pk=None, username=None, *args, **kwargs):
        if pk:
            coder = get_object_or_404(Coder, pk=pk)
        elif username:
            coder = get_object_or_404(Coder, user__username=username)

        if request.user == coder.user:
            return render(request, self.rw_template_name, { 'coder': coder, 'form': self.form_class(instance=coder) })

        return render(request, self.ro_template_name, { 'coder': coder })

    def post(self, request, username, *args, **kwargs):
        coder = get_object_or_404(Coder, user__username=username)

        form = self.form_class(request.POST, instance=coder)

        if form.is_valid():
            form.save()
            messages.info(request, 'Successfully updated profile')

        return render(request, self.rw_template_name, { 'coder': coder, 'form': form })