from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.base import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator

from .models import Challenge, Participant, Rule, ChallengeComment, Entry
from .forms import ChallengeForm, ChallengeCommentForm, AddRuleFormset, AddRuleTemplateFormset, SubmitEntryForm

from apps.coder.models import Coder

class IndexView(generic.ListView):
    model = Challenge

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)

        if self.request.user.is_authenticated and not self.request.user.is_anonymous():
            context['challenges_im_in'] = Challenge.objects.filter(participant__coder=self.request.user.coder)

        return context

class DetailView(View):
    form_class = ChallengeForm
    comment_form_class = ChallengeCommentForm
    template_name = 'challenge/challenge_detail.html'

    def get(self, request, pk, *args, **kwargs):
        challenge = get_object_or_404(Challenge, pk=pk)
        data = self.get_data(request, challenge)
        data['comment_form'] = self.comment_form_class()
        return render(request, self.template_name, data)

    def get_data(self, request, challenge):
        data = { 'challenge': challenge }
        data['now'] = timezone.now()
        data['challenge'] = challenge

        if request.user.is_authenticated() and not request.user.is_anonymous() and Coder.objects.filter(user=request.user).exists():
            data['form'] = self.form_class()
            data['challenges_im_in'] = Challenge.objects.filter(participant__coder=request.user.coder)
            data['is_owner'] = challenge.owner == request.user.coder
            data['can_comment'] = True

            participant_query = challenge.participant_set.filter(coder=request.user.coder)
            if participant_query.exists():
                data['participant'] = participant_query[0]

        return data

class UpdateView(View):
    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        challenge = get_object_or_404(Challenge, pk=pk)

        if (challenge.owner == request.user.coder):
            setattr(challenge, request.POST['name'], request.POST['value'])
            challenge.save()
            return HttpResponse('Challenge updated.')
        else:
            return HttpResponse('Can not update a challenge that you do not own.')

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
        challenge = Challenge(owner=request.user.coder)
        form = self.form_class(request.POST, instance=challenge)
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

class SubmitComment(View):
    form_class = ChallengeCommentForm

    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        comment = ChallengeComment(challenge_id=pk, coder=request.user.coder)
        form = self.form_class(request.POST, instance=comment)

        if form.is_valid():
            form.save()
            messages.info(request, 'Submitted comment')
        else:
            messages.warning(request, 'Can\'t submit an empty comment. You have been reported to the authorities.')

        return HttpResponseRedirect(reverse('challenge:detail', args=(pk,)))

class SubmitEntry(View):
    template_name = 'challenge/submit_entry.html'
    form_class = SubmitEntryForm

    def get(self, request, pk, *args, **kwargs):
        form = self.form_class()
        challenge = get_object_or_404(Challenge, pk=pk)
        return render(request, self.template_name, { 'form': form, 'challenge': challenge })

    def post(self, request, pk, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        challenge = get_object_or_404(Challenge, pk=pk)

        if form.is_valid():
            entry = form.save(commit=False)
            entry.challenge = challenge
            entry.participant = challenge.participant_set.get(coder__user=request.user)
            entry.save()
            messages.info(request, 'Submitted your entry!')
            return HttpResponseRedirect(reverse('challenge:detail', args=(pk,)))

        return render(request, self.template_name, { 'form': form, 'challenge': challenge })

class EntryDetail(View):
    template_name = 'challenge/entry_detail.html'

    def get_data(self, pk, epk):
        entry = get_object_or_404(Entry, pk=epk)
        challenge = get_object_or_404(Challenge, pk=pk)
        return { 'challenge': challenge, 'entry': entry }

    def get(self, request, pk, epk, *args, **kwargs):
        return render(request, self.template_name, self.get_data(pk, epk))