from django.conf import settings
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.conf.urls.static import static

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
    url(r'^ccauth/', include('apps.ccauth.urls', namespace='auth')),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)