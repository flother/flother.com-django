from django.conf.urls.defaults import patterns, url
from django.contrib.syndication.views import feed

from flother.apps.blog import views
from flother.apps.blog.feeds import LatestEntries


feeds = {
    'latest': LatestEntries,
}


urlpatterns = patterns('',
    url(r'^$', views.entry_index, name='blog_entry_index'),
    url(r'^(?P<year>\d{4})/$', views.entry_archive_year,
        name='blog_entry_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<slug>[a-z0-9\-]+)/$', views.entry_detail,
        name='blog_entry_detail'),
    url(r'^feeds/(.*)/$', feed, {'feed_dict': feeds}, name='blog_feeds'),
)
