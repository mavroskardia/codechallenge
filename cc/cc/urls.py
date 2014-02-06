from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'apps.landing.views.home', name='home'),
    url(r'^landing/', include('apps.landing.urls', namespace='landing')),
    url(r'^coder/', include('apps.coder.urls', namespace='coder')),
    url(r'^challenge/', include('apps.challenge.urls', namespace='challenge')),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', { 'template_name': 'coder/login.html' }, name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)
