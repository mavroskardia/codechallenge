from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.views.generic.base import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Challenge
from .forms import ChallengeForm


class IndexView(generic.ListView):
	model = Challenge

class DetailView(generic.DetailView):
	model = Challenge

class CreateView(View):
    form_class = ChallengeForm
    template_name = 'challenge/challenge_create.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, { 'form': form })

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            messages.info(request, 'Challenge created!')
            return HttpResponseRedirect(reverse('challenge:index'))

        return render(request, self.template_name, { 'form': form })
