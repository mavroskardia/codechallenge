from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from ..models import ChallengeComment
from ..forms import ChallengeCommentForm


class SubmitComment(generic.View):
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
