from django.conf.urls import patterns, url

from UserAPI import views

urlpatterns = patterns('',
    url(r'^create/$', views.create, name='create'),
    url(r'^details/$', views.details, name='details'),
	url(r'^listFollowers/$', views.listFollowers, name='listFollowers'),
	url(r'^listFollowing/$', views.listFollowing, name='listFollowing'),
)