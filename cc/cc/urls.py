from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import main.views
import main.urls


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', main.views.home, name='home'),
    url(r'^main/', include(main.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social_auth.urls')),
)
