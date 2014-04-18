from django.conf.urls import patterns, url

from Forum import views
from Views import userView
from Views import forumView
from Views import threadView
from Views import postView

urlpatterns = patterns('',
	#clear db
	url(r'^clear$', views.clear, name='clear'),

	#user
    url(r'^user/create/$', userView.create, name='userCreate'),
    url(r'^user/details/$', userView.details, name='userDetails'),
	url(r'^user/listFollowers/$', userView.listFollowers, name='userListFollowers'),
	url(r'^user/listFollowing/$', userView.listFollowing, name='userListFollowing'),
	url(r'^user/follow/$', userView.follow, name='userFollow'),
	url(r'^user/unfollow/$', userView.unfollow, name='userUnfollow'),
	url(r'^user/updateProfile/$', userView.updateProfile, name='userUpdateProfile'),
	url(r'^user/listPosts/$', userView.listPosts, name='userListPosts'),

	#forum
	url(r'^forum/create/$', forumView.create, name='forumCreate'),
	url(r'^forum/details/$', forumView.details, name='forumDetails'),
	url(r'^forum/listPosts/$', forumView.listPosts, name='forumListPosts'),
	url(r'^forum/listThreads/$', forumView.listThreads, name='forumListThreads'),
	url(r'^forum/listUsers/$', forumView.listUsers, name='forumListUsers'),

	#thread
	url(r'^thread/create/$', threadView.create, name='threadCreate'),
	url(r'^thread/details/$', threadView.details, name='threadDetails'),
	url(r'^thread/close/$', threadView.close, name='threadClose'),
	url(r'^thread/open/$', threadView.open, name='threadOpen'),
	url(r'^thread/list/$', threadView.list, name='threadList'),
	url(r'^thread/listPosts/$', threadView.listPosts, name='threadListPosts'),
	url(r'^thread/remove/$', threadView.remove, name='threadRemove'),
	url(r'^thread/restore/$', threadView.restore, name='threadRestore'),
	url(r'^thread/subscribe/$', threadView.subscribe, name='threadSubscribe'),
	url(r'^thread/unsubscribe/$', threadView.unsubscribe, name='threadUnsubscribe'),
	url(r'^thread/update/$', threadView.update, name='threadUpdate'),
	url(r'^thread/vote/$', threadView.vote, name='threadVote'),


	#post
	url(r'^post/create/$', postView.create, name='postCreate'),
	url(r'^post/details/$', postView.details, name='postDetails'),
	url(r'^post/list/$', postView.list, name='postList'),
	url(r'^post/remove/$', postView.remove, name='postRemove'),
	url(r'^post/restore/$', postView.restore, name='postRestore'),
	url(r'^post/update/$', postView.update, name='postUpdate'),
	url(r'^post/vote/$', postView.vote, name='postVote'),
)