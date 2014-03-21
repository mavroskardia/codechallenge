from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from ..models import Challenge
from ..forms import ChallengeForm, ChallengeCommentForm

from apps.coder.models import Coder


class DetailView(generic.View):
    form_class = ChallengeForm
    comment_form_class = ChallengeCommentForm
    template_name = 'challenge/challenge_detail.html'

    def get(self, request, pk, *args, **kwargs):
        challenge = get_object_or_404(Challenge, pk=pk)
        data = self.get_data(request, challenge)
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
            data['comment_form'] = self.comment_form_class()

            participant_query = challenge.participant_set.filter(coder=request.user.coder)
            if participant_query.exists():
                data['participant'] = participant_query[0]

        return data
