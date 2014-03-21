from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.core.urlresolvers import reverse

from ..models import Challenge
from ..forms import ChallengeForm, ChallengeCommentForm, AddRuleFormset

class MaintainView(generic.View):
    form_class = ChallengeForm
    comment_form_class = ChallengeCommentForm
    template_name = 'challenge/challenge_maintain.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        challenge = get_object_or_404(Challenge, pk=pk)
        is_owner = challenge.owner == request.user.coder
        if not is_owner:
            messages.error(request, 'You can not alter a challenge you do not own.')
            return HttpResponseRedirect(reverse('challenge:index'))

        data = {
            'challenge': challenge,
            'is_owner': is_owner,
            'form': self.form_class(instance=challenge),
            'rule_formset': AddRuleFormset(instance=challenge)
        }
        return render(request, self.template_name, data)

    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        challenge = get_object_or_404(Challenge, pk=pk)
        if challenge.owner != request.user.coder:
            messages.error(request, 'You can not alter a challenge you do not own.')
            return HttpResponseRedirect(reverse('challenge:index'))

        form = self.form_class(request.POST, instance=challenge)
        rule_formset = AddRuleFormset(request.POST)

        if form.is_valid():
            challenge = form.save()

            rule_formset = AddRuleFormset(request.POST, instance=challenge)
            if rule_formset.is_valid():
                rule_formset.save()

                messages.info(request, 'Challenge updated!')
                return HttpResponseRedirect(reverse('challenge:maintain', args=(pk,)))

        return render(request, self.template_name, { 'form': form, 'rule_formset': rule_formset })
