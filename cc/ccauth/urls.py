from django.conf.urls import patterns, include, url

import ccauth.views

urlpatterns = patterns('',
    url(r'^$', ccauth.views.main, name='ccauth'),
)
