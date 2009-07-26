from django.conf.urls.defaults import patterns, url

from flother.apps.search import views


urlpatterns = patterns('',
    url(r'^$', views.search_results, name='search_search_results'),
)
