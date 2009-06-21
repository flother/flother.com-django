from django.conf.urls.defaults import patterns, url

from flother.apps.contact import views

urlpatterns = patterns('',
    url(r'^$', views.send_message, name='contact_send_message'),
)
