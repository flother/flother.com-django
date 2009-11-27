import datetime

from django.conf import settings
from django.conf.urls.defaults import url, include, patterns, handler404, \
    handler500
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic.simple import direct_to_template, redirect_to

import flother
from flother.apps.blog.sitemaps import EntrySitemap


sitemaps = {
    'blog': EntrySitemap,
}
admin.autodiscover()


urlpatterns = patterns('',
    (r'^$', redirect_to, {'url': '/blog/', 'permanent': False}),
    (r'^blog/', include('flother.apps.blog.urls')),
    (r'^photos/', include('flother.apps.photos.urls')),
    (r'^contact/', include('flother.apps.contact.urls')),
    (r'^search/', include('flother.apps.search.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    url(r'^about/$', direct_to_template, {'template': 'about.html',
        'extra_context': {'birthday': datetime.date(1979, 8, 19),
        'version': flother.version()}}, name='about'),
    (r'^sitemap/$', sitemap, {'sitemaps': sitemaps}),
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('flother.apps.files.urls')),
)


if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', serve, {'document_root':
            settings.MEDIA_ROOT}),
    )
