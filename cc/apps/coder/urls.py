from django.conf.urls import patterns, include, url

from apps.coder.views.profile import ProfileView
from apps.coder.views.index import IndexView


urlpatterns = patterns('',
	url(r'^$', IndexView.as_view(), name='index'),
	url(r'^profile/(?P<username>\w+)$', ProfileView.as_view(), name='profile'),
)
