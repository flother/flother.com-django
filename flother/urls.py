import datetime

from django.conf import settings
from django.conf.urls.defaults import url, include, patterns, handler404, \
    handler500
from django.contrib import admin
from django.views.generic.simple import direct_to_template, redirect_to


admin.autodiscover()


urlpatterns = patterns('',
    (r'^$', redirect_to, {'url': '/blog/', 'permanent': False}),
    (r'^blog/', include('flother.apps.blog.urls')),
    (r'^contact/', include('flother.apps.contact.urls')),
    (r'^search/', include('flother.apps.search.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    url(r'^about/$', direct_to_template, {'template': 'about.html',
        'extra_context': {'birthday': datetime.date(1979, 8, 19)}},
        name='about'),
    (r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', serve, {'document_root':
            settings.MEDIA_ROOT}),
    )
