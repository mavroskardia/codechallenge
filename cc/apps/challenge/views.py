from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
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

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['already_joined'] = Challenge.objects.filter(coder__user__id=self.request.user.id).exists()
        return context

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

class JoinView(View):

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        challenge = get_object_or_404(Challenge, pk=pk)
        if challenge.coder_set.filter(pk=request.user.coder.id).exists():
            messages.error(request, 'Trying to join a challenge you are already participating in. Contacting the NSA and FBI and CIA.')
        else:
            challenge.coder_set.add(request.user.coder)
            challenge.save()
            messages.info(request, 'Joined Challenge!')

        return HttpResponseRedirect(reverse('challenge:detail', args=(pk,)))
