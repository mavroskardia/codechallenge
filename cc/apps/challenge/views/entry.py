import os
from io import BytesIO
from PIL import Image

from django.http import HttpResponseRedirect
from django.views import generic
from django.core.files import File
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404

from ..models import Challenge, Entry
from ..forms import SubmitEntryForm, SubmitEntryCommentForm, SubmitEntryScreenshotForm

from apps.coder.models import Coder


class SubmitEntry(generic.View):
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
            return HttpResponseRedirect(reverse('challenge:entry', args=(pk,entry.id,)))

        return render(request, self.template_name, { 'form': form, 'challenge': challenge })

class EntryDetail(generic.View):
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


class SubmitEntryComment(generic.View):
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

class SubmitEntryScreenshot(generic.View):
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

