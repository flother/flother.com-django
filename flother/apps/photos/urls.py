from django.conf.urls.defaults import patterns, url

from flother.apps.photos import views


urlpatterns = patterns('',
    url(r'^archive/(?P<year>\d{4})/(?P<slug>[a-z0-9\-]+)/$',
        views.photo_detail, name='photos_photo_detail'),
)
