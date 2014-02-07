from django.conf.urls import patterns, include, url

from apps.ccauth.views.login import LoginView, LogoutView
from apps.ccauth.views.register import RegisterView


urlpatterns = patterns('',
	url(r'^login/$', LoginView.as_view(), name='login'),
	url(r'^logout/$', LogoutView.as_view(), name='logout'),
	url(r'^register/$', RegisterView.as_view(), name='register'),
)
