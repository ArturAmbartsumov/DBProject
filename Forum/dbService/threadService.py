import json
import datetime
import time

from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, QueryDict
from django.db import connection
from django.db import transaction

from Forum.dbService.userService import *
from Forum.dbService.forumService import *
from Forum.dbService.functions import *

def threadCreate(request_data):
	try: 
		forum_short_name = request_data['forum']
		title = request_data['title']
		isClosed = request_data['isClosed']
		user_email = request_data['user']
		date = request_data['date']
		message = request_data['message']
		slug = request_data['slug']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}
	isDeleted = request_data.get('isDeleted', False)
	#date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

	get_user_id = getUserIDByEmail(user_email)
	if get_user_id['err'] != 0: return {'err': get_user_id['err']}
	user_id = get_user_id['user_id']

	get_forum_id = getForumIDByShortname(forum_short_name)
	if get_forum_id['err'] != 0: return {'err': get_forum_id['err']}
	forum_id = get_forum_id['forum_id']

	err = createNewThread({'forum': forum_id,
						   'user': user_id,
						   'title': title,
						   'isClosed': isClosed,
						   'date': date,
						   'message': message,
						   'slug': slug,
						   'isDeleted': isDeleted})
	if err['err'] != 0: return {'err': err['err']}

	get_thread = getThread({'user_id': user_id, 'date': date})
	if get_thread['err'] != 0: return {'err': get_thread['err']}
	thread = get_thread['thread']

	thread['user'] = user_email
	thread['forum'] = forum_short_name

	return {'err': 0, 'thread': thread}

def threadDetails(request_data):
	try: 
		thread_id = request_data['thread']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}
	related = request_data.getlist('related', [])

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

def threadOpenOrClose(request_data, option):
	try: 
		thread_id = request_data['thread']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	if option == 'close': status = 1
	if option == 'open': status = 0

	get_cursor = sendQuery("UPDATE Threads SET isClosed = %s WHERE id = %s", [status, thread_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	return {'err': 0, 'thread': {'thread': thread_id}}

def threadRemoveOrRestore(request_data, option):
	try: 
		thread_id = request_data['thread']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	if option == 'remove': status = 1
	if option == 'restore': status = 0

	get_cursor = sendQuery("UPDATE Threads SET isDeleted = %s WHERE id = %s", [status, thread_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	return {'err': 0, 'thread': {'thread': thread_id}}

def threadVote(request_data):
	try: 
		thread_id = request_data['thread']
		vote = request_data['vote']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	if vote == -1: get_cursor = sendQuery("UPDATE Threads SET dislikes = dislikes + 1 WHERE id = %s", [thread_id])
	if vote == 1: get_cursor = sendQuery("UPDATE Threads SET likes = likes + 1 WHERE id = %s", [thread_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}

	get_threadDetails = getThreadDetailsByID(thread_id)
	if get_threadDetails['err'] != 0: return {'err': get_threadDetails['err']}
	thread = get_threadDetails['thread']

	return {'err': 0, 'thread': thread}

def threadUpdate(request_data):
	try:
		message = request_data['message']
		slug = request_data['slug']
		thread_id = request_data['thread']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	get_cursor = sendQuery("UPDATE Threads SET message = %s, slug = %s WHERE id = %s", [message, slug, thread_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}

	get_threadDetails = getThreadDetailsByID(thread_id)
	if get_threadDetails['err'] != 0: return {'err': get_threadDetails['err']}
	thread = get_threadDetails['thread']

	return {'err': 0, 'thread': thread}

def threadSubscribeOrUnsubscribe(request_data, option):
	try:
		user_email = request_data['user']
		thread_id = request_data['thread']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	get_user_id = getUserIDByEmail(user_email)
	if get_user_id['err'] != 0: return {'err': get_user_id['err']}
	user_id = get_user_id['user_id']

	if option == 'subscribe':
		get_cursor = sendQuery("INSERT INTO Subscriptions (thread_id, user_id) VALUES (%s, %s)", [thread_id, user_id])
	if option == 'unsubscribe':
		get_cursor = sendQuery("DELETE FROM Subscriptions WHERE thread_id = %s AND user_id = %s", [thread_id, user_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}

	return {'err': 0, 'subscribe': {'thread': thread_id, 'user': user_email}}


def getThreadDetailsByID(thread_id):
	get_threadDetails = threadDetails(QueryDict('thread=' + str(thread_id)))
	if get_threadDetails['err'] != 0: return {'err': get_threadDetails['err']}
	thread = get_threadDetails['thread']
	return {'err': 0, 'thread': thread}

def createNewThread(data):
	get_cursor = sendQuery("INSERT INTO Threads (title, date, message, slug, isClosed, isDeleted, user, forum) " +\
						   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
						   [data['title'],
						   data['date'],
						   data['message'],
						   data['slug'],
						   data['isClosed'],
						   data['isDeleted'],
						   data['user'],
						   data['forum']])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	return {'err': 0}

def getThread(data):
	get_cursor = sendQuery("SELECT * FROM Threads WHERE user=%s AND date=%s", [data['user_id'], data['date']])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']

	if cursor.rowcount == 0: return {'err': "Thread whith user_id = " + str(data['user_id']) + " and date = " + data['date'] + " not found"}
	thread = dictfetchall(cursor)[0]
	thread['date'] = thread['date'].strftime("%Y-%m-%d %H:%M:%S")
	return {'err': 0, 'thread': thread}

def getThreadByID(thread_id):
	get_cursor = sendQuery("SELECT * FROM Threads WHERE id=%s", [thread_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']

	if cursor.rowcount != 1: return {'err': "Thread whith id = " + str(thread_id) + " not found"}
	thread = dictfetchall(cursor)[0]
	thread['date'] = thread['date'].strftime("%Y-%m-%d %H:%M:%S")
	return {'err': 0, 'thread': thread}

def getPostCountInThread(thread_id):
	get_cursor = sendQuery("SELECT count(*) AS posts FROM Posts WHERE thread = %s", [thread_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	
	if cursor.rowcount != 1: return {'err': "User whith email = " + email + " not found"}
	posts = transformToList(cursor.fetchall())
	return {'err': 0, 'posts': posts[0]}




















