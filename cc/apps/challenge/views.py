import os

from io import BytesIO
from PIL import Image

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.base import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.files import File
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator

from .models import Challenge, Participant, Rule, ChallengeComment, Entry
from .forms import ChallengeForm, ChallengeCommentForm
from .forms import AddRuleFormset, AddRuleTemplateFormset
from .forms import SubmitEntryForm, SubmitEntryCommentForm, SubmitEntryScreenshotForm

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

class UpdateRuleView(View):
    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        rule = get_object_or_404(Rule, pk=pk)

        if (rule.challenge.owner == request.user.coder):
            setattr(rule, request.POST['name'], request.POST['value'])
            rule.save()
            return HttpResponse('Rule updated.')
        else:
            return HttpResponse('Can not update a rule for a challenge that you do not own.')

class DeleteRuleView(View):
    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        rule = get_object_or_404(Rule, pk=pk)

        if (rule.challenge.owner == request.user.coder):
            rule.delete()
            return HttpResponse('yay')
        else:
            return HttpResponse('Can not delete a rule for a challenge that you do not own.')

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

        return render(request, self.template_name, { 'rule_formset': formset, 'rule_count': rule_count })

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
    comment_form = SubmitEntryCommentForm
    screenshot_form = SubmitEntryScreenshotForm

    def get_data(self, request, pk, epk):
        entry = get_object_or_404(Entry, pk=epk)
        challenge = get_object_or_404(Challenge, pk=pk)
        can_comment = request.user.is_authenticated() and Coder.objects.filter(user=request.user).exists()
        return {
            'challenge': challenge,
            'entry': entry,
            'can_comment': can_comment,
            'comment_form': self.comment_form(),
            'screenshot_form': self.screenshot_form()
        }

    def get(self, request, pk, epk, *args, **kwargs):
        return render(request, self.template_name, self.get_data(request, pk, epk))

class SubmitEntryComment(View):
    form_class = SubmitEntryCommentForm

    @method_decorator(login_required)
    def post(self, request, pk, epk, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.entry_id = epk
            comment.coder = request.user.coder
            comment.save()
            messages.info(request, 'Successfully commented')
        else:
            messages.warning(request, 'Can\'t submit an empty comment. You have been reported to the authorities.')

        return HttpResponseRedirect(reverse('challenge:entry', args=(pk, epk,)))

class SubmitEntryScreenshot(View):
    form_class = SubmitEntryScreenshotForm

    @method_decorator(login_required)
    def post(self, request, pk, epk, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        entry = get_object_or_404(Entry, pk=epk)

        if form.is_valid():
            ss = form.save(commit=False)
            ss.entry = entry
            name, thumb = self.generate_thumbnail(request, ss.pic)
            ss.thumbnail.save(name, thumb)
            ss.save()
            messages.info(request, 'Successfully submitted screenshot')
        else:
            messages.warning(request, 'Screenshot failed to upload: forgot to specify a file')

        return HttpResponseRedirect(reverse('challenge:entry', args=(pk,epk,)))


    def generate_thumbnail(self, request, pic):
        splits = os.path.splitext(os.path.split(pic.name)[-1])
        name = splits[0] + '_resized' + splits[1]

        fakefile = BytesIO()

        img = Image.open(pic.file)
        img.thumbnail((320,240), Image.ANTIALIAS)
        img.save(fakefile, format=img.format)

        return name, File(fakefile)

