import datetime
import time

from django.db import IntegrityError
from Forum.dbService import functions as Util

def getFollowers(data):
	get_cursor = Util.sendQuery("SELECT id, username, email, name, about, isAnonymous " +\
						   "FROM Users, (" +\
						       "SELECT follower_id FROM Followers WHERE user_id = %s AND follower_id >= %s" +\
						   ") AS T " +\
						   "WHERE Users.id = T.follower_id " +\
						   "ORDER BY Users.name " + data['order'] +\
						   " LIMIT %s", [data['user_id'], data['since_id'], data['limit']])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	return {'err': 0, 'followList': Util.dictfetchall(cursor)}

def getFollowing(data):
	get_cursor = Util.sendQuery("SELECT id, username, email, name, about, isAnonymous " +\
						   "FROM Users, (" +\
						       "SELECT follower_id FROM Followers WHERE user_id = %s AND follower_id >= %s" +\
						   ") AS T " +\
						   "WHERE Users.id = T.follower_id " +\
						   "ORDER BY Users.name " + data['order'] +\
						   " LIMIT %s", [data['user_id'], data['since_id'], data['limit']])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	return {'err': 0, 'followList': Util.dictfetchall(cursor)}

def getFollowersEmails(user_id):
	get_cursor = Util.sendQuery("SELECT Users.email AS emails FROM Users, " +\
						   "(SELECT follower_id FROM Followers WHERE user_id = %s) AS T " +\
						   "WHERE Users.id = T.follower_id", [user_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	return {'err': 0, 'followers': Util.transformToList(cursor.fetchall())}

def getFollowingEmails(user_id):
	get_cursor = Util.sendQuery("SELECT Users.email AS emails FROM Users, " +\
						   "(SELECT user_id FROM Followers WHERE follower_id = %s) AS T " +\
						   "WHERE Users.id = T.user_id", [user_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	return {'err': 0, 'followers': Util.transformToList(cursor.fetchall())}	

def getSubscriptionsID(user_id):
	get_cursor = Util.sendQuery("SELECT thread_id FROM Subscriptions WHERE user_id = %s", [user_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	return {'err': 0, 'subscriptions': Util.transformToList(cursor.fetchall())}

def getUserIDByEmail(email):
	get_cursor = Util.sendQuery("SELECT id FROM Users WHERE email = %s", [email])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	
	if cursor.rowcount != 1: return {'err': "User whith email = " + email + " not found"}
	users_id = Util.transformToList(cursor.fetchall())
	return {'err': 0, 'user_id': users_id[0]}

def getUserEmailByID(user_id):
	get_cursor = Util.sendQuery("SELECT email FROM Users WHERE id = %s", [user_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	
	if cursor.rowcount != 1: return {'err': "User whith ID = " + str(user_id) + " not found"}
	email = Util.transformToList(cursor.fetchall())
	return {'err': 0, 'email': email[0]}

def getUserById(user_id):
	get_cursor = Util.sendQuery("SELECT * FROM Users WHERE id=%s", [user_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	
	if cursor.rowcount != 1: return {'err': "User whith ID = " + str(user_id) + " not found"}
	return {'err': 0, 'user': Util.dictfetchall(cursor)[0]}

def getUserDetailsById(user_id):
	get_user = getUserById(user_id)
	if get_user['err'] != 0: return {'err': get_user['err']}
	user = get_user['user']

	get_fullUser = buildFullUserDetails(user)
	if get_fullUser['err'] != 0: return {'err': get_fullUser['err']}
	fullUser = get_fullUser['user']

	return {'err': 0, 'user': fullUser}

def buildFullUserDetails(user):
	get_followers = getFollowersEmails(user['id'])
	if get_followers['err'] != 0: return {'err': get_followers['err']}
	followers = get_followers['followers']

	get_following = getFollowingEmails(user['id'])
	if get_following['err'] != 0: return {'err': get_following['err']}
	following = get_following['followers']

	get_subscriptions = getSubscriptionsID(user['id'])
	if get_subscriptions['err'] != 0: return {'err': get_subscriptions['err']}
	subscriptions = get_subscriptions['subscriptions']

	user['followers'] = followers
	user['following'] = following
	user['subscriptions'] = subscriptions
	
	return {'err': 0, 'user': user}

def getForumByID(forum_id):
	get_cursor = Util.sendQuery("SELECT * FROM Forums WHERE id=%s", [forum_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']

	if cursor.rowcount != 1: return {'err': "Forum whith id = " + str(forum_id) + " not found"}
	return {'err': 0, 'forum': Util.dictfetchall(cursor)[0]}

def getForumDetailsById(forum_id):
	get_forum = getForumByID(forum_id)
	if get_forum['err'] != 0: return {'err': get_forum['err']}
	forum = get_forum['forum']

	get_user = getUserEmailByID(forum['user'])
	if get_user['err'] != 0: return {'err': get_user['err']}
	user = get_user['email']

	forum['user'] = user
	return {'err': 0, 'forum': forum}

def getForumIDByShortname(short_name):
	get_cursor = Util.sendQuery("SELECT id FROM Forums WHERE short_name = %s", [short_name])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	
	if cursor.rowcount != 1: return {'err': "Forum whith short_name = " + short_name + " not found"}
	forum_id = Util.transformToList(cursor.fetchall())
	return {'err': 0, 'forum_id': forum_id[0]}

def getShortnameByForumID(forum_id):
	get_cursor = Util.sendQuery("SELECT short_name FROM Forums WHERE id = %s", [forum_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	
	if cursor.rowcount != 1: return {'err': "Forum whith id = " + str(forum_id) + " not found"}
	short_name = Util.transformToList(cursor.fetchall())
	return {'err': 0, 'short_name': short_name[0]}

def getPostCountInThread(thread_id):
	get_cursor = Util.sendQuery("SELECT count(*) AS posts FROM Posts WHERE thread = %s", [thread_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	
	if cursor.rowcount != 1: return {'err': "User whith email = " + email + " not found"}
	posts = Util.transformToList(cursor.fetchall())
	return {'err': 0, 'posts': posts[0]}

def getThreadByID(thread_id):
	get_cursor = Util.sendQuery("SELECT * FROM Threads WHERE id=%s", [thread_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']

	if cursor.rowcount != 1: return {'err': "Thread whith id = " + str(thread_id) + " not found"}
	thread = Util.dictfetchall(cursor)[0]
	thread['date'] = thread['date'].strftime("%Y-%m-%d %H:%M:%S")
	return {'err': 0, 'thread': thread}

def getThreadDetailsByID(thread_id, related):
	get_thread = getThreadByID(thread_id)
	if get_thread['err'] != 0: return {'err': get_thread['err']}
	thread = get_thread['thread']

	if 'user' in related:
		get_user = getUserDetailsById(thread['user'])
		if get_user['err'] != 0: return {'err': get_user['err']}
		user = get_user['user']
	else:
		get_user = getUserEmailByID(thread['user'])
		if get_user['err'] != 0: return {'err': get_user['err']}
		user = get_user['email']

	if 'forum' in related:
		get_forum = getForumDetailsById(thread['forum'])
		if get_forum['err'] != 0: return {'err': get_forum['err']}
		forum = get_forum['forum']
	else:
		get_forum = getShortnameByForumID(thread['forum'])
		if get_forum['err'] != 0: return {'err': get_forum['err']}
		forum = get_forum['short_name']

	get_posts = getPostCountInThread(thread_id)
	if get_posts['err'] != 0: return {'err': get_posts['err']}
	posts = get_posts['posts']

	thread['user'] = user
	thread['forum'] = forum
	thread['points'] = thread['likes'] - thread['dislikes']
	thread['posts'] = posts

	return {'err': 0, 'thread': thread}

def getPostByID(post_id):
	get_cursor = Util.sendQuery("SELECT * FROM Posts WHERE id=%s", [post_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']

	if cursor.rowcount != 1: return {'err': "Post whith id = " + str(post_id) + " not found"}
	post = Util.dictfetchall(cursor)[0]
	post['date'] = post['date'].strftime("%Y-%m-%d %H:%M:%S")
	return {'err': 0, 'post': post}

def getPostDetailsByID(post_id, related):
	get_post = getPostByID(post_id)
	if get_post['err'] != 0: return {'err': get_post['err']}
	post = get_post['post']

	if 'user' in related:
		get_user = getUserDetailsById(post['user'])
		if get_user['err'] != 0: return {'err': get_user['err']}
		user = get_user['user']
	else:
		get_user = getUserEmailByID(post['user'])
		if get_user['err'] != 0: return {'err': get_user['err']}
		user = get_user['email']

	if 'forum' in related:
		get_forum = getForumDetailsById(post['forum'])
		if get_forum['err'] != 0: return {'err': get_forum['err']}
		forum = get_forum['forum']
	else:
		get_forum = getShortnameByForumID(post['forum'])
		if get_forum['err'] != 0: return {'err': get_forum['err']}
		forum = get_forum['short_name']

	if 'thread' in related:
		get_thread = getThreadDetailsByID(post['thread'], [])
		if get_thread['err'] != 0: return {'err': get_thread['err']}
		thread = get_thread['thread']
		post['thread'] = thread

	post['user'] = user
	post['forum'] = forum
	post['points'] = post['likes'] - post['dislikes']
	return {'err': 0, 'post': post}


def getListPosts(entity, options):
	limit = options['limit']
	order = options['order']
	since = options['since']
	query = ("SELECT * FROM Posts " +\
			"INNER JOIN (SELECT id AS forum_id, short_name AS forum_short_name FROM Forums) AS Forums " +\
			"ON Forums.forum_id = Posts.forum " +\
			"INNER JOIN (SELECT id AS user_id, email AS user_email FROM Users) AS Users " +\
			"ON Users.user_id = Posts.user " +\
			"WHERE " + entity['field'] + " = %s AND Posts.date >= %s " +\
			"ORDER BY date " + order +\
			" LIMIT %s")
	get_cursor = Util.sendQuery(query, [entity['key'], since, limit])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	listPosts = Util.dictfetchall(cursor)
	for post in listPosts:
		post.pop('user_id')
		post.pop('forum_id')
		post['user'] = post.pop('user_email')
		post['forum'] = post.pop('forum_short_name')
		post['points'] = post['likes'] - post['dislikes']
		post['date'] = post['date'].strftime("%Y-%m-%d %H:%M:%S")
	return {'err': 0, 'listPosts': listPosts}

def getListPostsInForum(forum, related, options):
	limit = options['limit']
	order = options['order']
	since = options['since']

	get_forum = getForumIDByShortname(forum)
	if get_forum['err'] != 0: return {'err': get_forum['err']}
	forum_id = get_forum['forum_id']
	query = ("SELECT * FROM Posts " +\
			"WHERE forum = %s AND Posts.date >= %s " +\
			"ORDER BY date " + order +\
			" LIMIT 2")
	get_cursor = Util.sendQuery(query, [forum_id, since])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	listPosts = Util.dictfetchall(cursor)

	for post in listPosts:
		if 'user' in related:
			get_user = getUserDetailsById(post['user'])
			if get_user['err'] != 0: return {'err': get_user['err']}
			user = get_user['user']
		else:
			get_user = getUserEmailByID(post['user'])
			if get_user['err'] != 0: return {'err': get_user['err']}
			user = get_user['email']

		if 'forum' in related:
			get_forum = getForumDetailsById(post['forum'])
			if get_forum['err'] != 0: return {'err': get_forum['err']}
			forum = get_forum['forum']

		if 'thread' in related:
			get_thread = getThreadDetailsByID(post['thread'], [])
			if get_thread['err'] != 0: return {'err': get_thread['err']}
			thread = get_thread['thread']
			post['thread'] = thread

		post['user'] = user
		post['forum'] = forum
		post['points'] = post['likes'] - post['dislikes']
		post['date'] = post['date'].strftime("%Y-%m-%d %H:%M:%S")
	return {'err': 0, 'listPosts': listPosts}

