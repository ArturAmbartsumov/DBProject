from django.conf.urls import patterns, url

from UserAPI import views

urlpatterns = patterns('',
    url(r'^create/$', views.create, name='create'),
    url(r'^details/$', views.details, name='details'),
)