from django.conf import settings
from django.conf.urls.defaults import include, patterns, handler404, handler500
from django.contrib import admin
from django.views.generic.simple import direct_to_template

from flother.apps.contact.forms import MessageForm


admin.autodiscover()
contact_form = MessageForm()


urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template': 'home.html',
        'extra_context': {'form': contact_form}}),
    (r'^blog/', include('flother.apps.blog.urls')),
    (r'^contact/', include('flother.apps.contact.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', serve, {'document_root':
            settings.MEDIA_ROOT}),
    )
