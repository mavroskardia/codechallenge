from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.base import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Challenge, Participant, Rule
from .forms import ChallengeForm, AddRuleFormset, AddRuleTemplateFormset


class IndexView(generic.ListView):
    model = Challenge

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)

        if self.request.user.is_authenticated and not self.request.user.is_anonymous():
            context['challenges_im_in'] = Challenge.objects.filter(participant__coder=self.request.user.coder)

        return context

class DetailView(generic.DetailView):
    model = Challenge

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        challenge = context['object']

        context['owner'] = challenge.participant_set.get(is_owner=True)
        context['participant'] = challenge.participant_set.filter(coder=self.request.user.coder)
        context['already_joined'] = context['participant'].exists()
        context['challenge'] = challenge

        return context

class CreateView(View):
    form_class = ChallengeForm
    template_name = 'challenge/challenge_create.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        rule_formset = AddRuleFormset(instance=Challenge())

        return render(request, self.template_name, { 'form': form, 'rule_formset': rule_formset })

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        rule_formset = AddRuleFormset(request.POST)

        if form.is_valid():
            challenge = form.save()

            # todo: move this to the Challenge clean() or save() method
            participant = Participant(coder=request.user.coder, challenge=challenge, is_owner=True)
            participant.save()

            rule_formset = AddRuleFormset(request.POST, instance=challenge)
            if rule_formset.is_valid():
                rule_formset.save()

                messages.info(request, 'Challenge created!')
                return HttpResponseRedirect(reverse('challenge:index'))

        return render(request, self.template_name, { 'form': form, 'rule_formset': rule_formset })

class JoinView(View):
    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        challenge = get_object_or_404(Challenge, pk=pk)
        if challenge.participant_set.filter(coder=request.user.coder).exists():
            messages.error(request, 'Trying to join a challenge you are already participating in. Contacting the NSA and FBI and CIA.')
        else:
            p = Participant(coder=request.user.coder, challenge=challenge)
            p.save()
            messages.info(request, 'Joined Challenge!')

        return HttpResponseRedirect(reverse('challenge:detail', args=(pk,)))


class LeaveView(View):
    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        challenge = get_object_or_404(Challenge, pk=pk)
        cp = challenge.participant_set.filter(coder=request.user.coder)
        if cp.exists():
            cp.delete()
            messages.info(request, 'Left challenge.  Quitters never win.')
        else:
            messages.error(request, 'You had never joined this challenge.')

        return HttpResponseRedirect(reverse('challenge:detail', args=(pk,)))

class AddRuleTemplate(View):
    template_name = 'challenge/add_rule_template.html'

    @method_decorator(login_required)
    def get(self, request, rule_count, *args, **kwargs):
        rule_formset = AddRuleTemplateFormset(instance=Challenge())

        formset = rule_formset.form(
            auto_id=rule_formset.auto_id,
            prefix=rule_formset.add_prefix(rule_count),
            empty_permitted=True,
        )
        rule_formset.add_fields(formset, None)

        return render(request, self.template_name, { 'rule_formset': formset })