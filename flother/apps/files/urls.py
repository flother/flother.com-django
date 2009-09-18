from django.conf.urls.defaults import patterns, url

from flother.apps.files import views


urlpatterns = patterns('',
    # Some URL namespacing here: site the JSON view within the admin.
    url(r'^admin/files/file\.json$', views.files_list, name='files_file_list'),
)
