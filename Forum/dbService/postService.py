import json
import datetime
import time

from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, QueryDict
from django.db import connection
from django.db import transaction

from Forum.dbService.threadService import *
from Forum.dbService.userService import *
from Forum.dbService.forumService import *
from Forum.dbService.functions import *

def postCreate(request_data):
	try: 
		date = request_data['date']
		thread_id = request_data['thread']
		message = request_data['message']
		user_email = request_data['user']
		forum_short_name = request_data['forum']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}
	parent = request_data.get('parent', None)
	isApproved = request_data.get('isApproved', False)
	isHighlighted = request_data.get('isHighlighted', False)
	isEdited = request_data.get('isEdited', False)
	isSpam = request_data.get('isSpam', False)
	isDeleted = request_data.get('isDeleted', False)

	get_user_id = getUserIDByEmail(user_email)
	if get_user_id['err'] != 0: return {'err': get_user_id['err']}
	user_id = get_user_id['user_id']

	get_forum_id = getForumIDByShortname(forum_short_name)
	if get_forum_id['err'] != 0: return {'err': get_forum_id['err']}
	forum_id = get_forum_id['forum_id']

	err = createNewPost({'date': date,
						 'thread': thread_id,
						 'message': message,
						 'user': user_id,
						 'forum': forum_id,
						 'parent': parent,
						 'isApproved': isApproved,
						 'isHighlighted': isHighlighted,
						 'isEdited': isEdited,
						 'isSpam': isSpam,
						 'isDeleted': isDeleted})
	if err['err'] != 0: return {'err': err['err']}

	get_post = getPost({'user_id': user_id, 'date': date})
	if get_post['err'] != 0: return {'err': get_post['err']}
	post = get_post['post']

	post['user'] = user_email
	post['forum'] = forum_short_name

	return {'err': 0, 'post': post}

def postDetails(request_data):
	try: 
		post_id = request_data['post']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}
	related = request_data.getlist('related', [])

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
		get_thread = getThreadDetailsByID(post['thread'])
		if get_thread['err'] != 0: return {'err': get_thread['err']}
		thread = get_thread['thread']
		post['thread'] = thread

	post['user'] = user
	post['forum'] = forum
	post['points'] = post['likes'] - post['dislikes']
	return {'err': 0, 'post': post}

def postRemoveOrRestore(request_data, option):
	try: 
		post_id = request_data['post']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	if option == 'remove': status = 1
	if option == 'restore': status = 0

	get_cursor = sendQuery("UPDATE Posts SET isDeleted = %s WHERE id = %s", [status, post_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	return {'err': 0, 'post': {'post': post_id}}

def postVote(request_data):
	try: 
		post_id = request_data['post']
		vote = request_data['vote']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	if vote == -1: get_cursor = sendQuery("UPDATE Posts SET dislikes = dislikes + 1 WHERE id = %s", [post_id])
	if vote == 1: get_cursor = sendQuery("UPDATE Posts SET likes = likes + 1 WHERE id = %s", [post_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}

	get_postDetails = getPostDetailsByID(post_id)
	if get_postDetails['err'] != 0: return {'err': get_postDetails['err']}
	post = get_postDetails['post']

	return {'err': 0, 'post': post}

def postUpdate(request_data):
	try:
		message = request_data['message']
		post_id = request_data['thread']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	get_cursor = sendQuery("UPDATE Posts SET message = %s WHERE id = %s", [message, post_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}

	get_postDetails = getPostDetailsByID(post_id)
	if get_postDetails['err'] != 0: return {'err': get_postDetails['err']}
	post = get_postDetails['post']

	return {'err': 0, 'post': post}

def createNewPost(data):
	get_cursor = sendQuery("INSERT INTO Posts (date, message, isApproved, isHighlighted, isEdited, isSpam, isDeleted, parent, user, forum, thread) " +\
						   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
						   [data['date'],
						   data['message'],
						   data['isApproved'],
						   data['isHighlighted'],
						   data['isEdited'],
						   data['isSpam'],
						   data['isDeleted'],
						   data['parent'],
						   data['user'],
						   data['forum'],
						   data['thread']])
	if get_cursor['err'] != 0:
		print "sdfsf"
		return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	return {'err': 0}

def getPost(data):
	get_cursor = sendQuery("SELECT * FROM Posts WHERE user=%s AND date=%s", [data['user_id'], data['date']])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']

	if cursor.rowcount == 0: return {'err': "Post whith user_id = " + str(data['user_id']) + " and date = " + data['date'] + " not found"}
	post = dictfetchall(cursor)[0]
	post['date'] = post['date'].strftime("%Y-%m-%d %H:%M:%S")
	return {'err': 0, 'post': post}

def getPostByID(post_id):
	get_cursor = sendQuery("SELECT * FROM Posts WHERE id=%s", [post_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']

	if cursor.rowcount != 1: return {'err': "Post whith id = " + str(post_id) + " not found"}
	post = dictfetchall(cursor)[0]
	post['date'] = post['date'].strftime("%Y-%m-%d %H:%M:%S")
	return {'err': 0, 'post': post}

def getPostDetailsByID(post_id):
	get_postDetails = postDetails(QueryDict('post=' + str(post_id)))
	if get_postDetails['err'] != 0: return {'err': get_postDetails['err']}
	post = get_postDetails['post']
	return {'err': 0, 'post': post}

def getListPosts(entity, options, related):
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
	get_cursor = sendQuery(query, [entity['key'], since, limit])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	listPosts = dictfetchall(cursor)
	for post in listPosts:
		post.pop('user_id')
		post.pop('forum_id')
		post['user'] = post.pop('user_email')
		post['forum'] = post.pop('forum_short_name')
		post['points'] = post['likes'] - post['dislikes']
		post['date'] = post['date'].strftime("%Y-%m-%d %H:%M:%S")
	return {'err': 0, 'listPosts': listPosts}

def getListPostsInForim(forum, options, related):
	limit = options['limit']
	order = options['order']
	since = options['since']

	get_forum = getForumIDByShortname(forum)
	if get_forum['err'] != 0: return {'err': get_forum['err']}
	forum_id = get_forum['forum_id']
	query = ("SELECT * FROM Posts " +\
			"WHERE forum = %s AND Posts.date >= %s " +\
			"ORDER BY date " + order +\
			" LIMIT %s")
	get_cursor = sendQuery(query, [forum_id, since, limit])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	listPosts = dictfetchall(cursor)

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
			get_thread = getThreadDetailsByID(post['thread'])
			if get_thread['err'] != 0: return {'err': get_thread['err']}
			thread = get_thread['thread']
			post['thread'] = thread

		post['user'] = user
		post['forum'] = forum
		post['points'] = post['likes'] - post['dislikes']
		post['date'] = post['date'].strftime("%Y-%m-%d %H:%M:%S")
	return {'err': 0, 'listPosts': listPosts}


