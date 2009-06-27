from django.conf.urls.defaults import patterns, url

from flother.apps.blog import views


urlpatterns = patterns('',
    url(r'^$', views.entry_index, name='blog_entry_index'),
    url(r'^(?P<year>\d{4})/$', views.entry_archive_year,
        name='blog_entry_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<slug>[a-z0-9\-]+)/$', views.entry_detail,
        name='blog_entry_detail'),
)
