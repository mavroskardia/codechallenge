from django.views import generic

from ..models import Challenge

class IndexView(generic.ListView):
    model = Challenge

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)

        if self.request.user.is_authenticated and not self.request.user.is_anonymous():
            context['challenges_im_in'] = Challenge.objects.filter(participant__coder=self.request.user.coder)

        return context

