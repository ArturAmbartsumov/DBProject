from django.conf.urls import patterns, url

from forumViews import userView

urlpatterns = patterns('',
    url(r'^user/create/$', userView.create, name='userCreate'),
    url(r'^user/details/$', userView.details, name='userDetails'),
	url(r'^user/listFollowers/$', userView.listFollowers, name='userListFollowers'),
	url(r'^user/listFollowing/$', userView.listFollowing, name='userListFollowing'),
	url(r'^user/follow/$', userView.follow, name='userFollow'),
	url(r'^user/unfollow/$', userView.unfollow, name='userUnfollow'),
	url(r'^user/updateProfile/$', userView.updateProfile, name='userUpdateProfile'),
)