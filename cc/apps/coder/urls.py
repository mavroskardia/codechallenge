from django.conf.urls import patterns, include, url

from apps.coder.views.profile import ProfileView


urlpatterns = patterns('',
	url(r'^profile/(?P<username>\w+)$', ProfileView.as_view(), name='profile'),
)
