import datetime
import time

from django.db import IntegrityError

from Forum.dbService import service as Serv
from Forum.dbService import functions as Util

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

	get_user_id = Serv.getUserIDByEmail(user_email)
	if get_user_id['err'] != 0: return {'err': get_user_id['err']}
	user_id = get_user_id['user_id']

	get_forum_id = Serv.getForumIDByShortname(forum_short_name)
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

	get_threadDetails = Serv.getThreadDetailsByID(thread_id, related)
	if get_threadDetails['err'] != 0: return {'err': get_threadDetails['err']}
	thread = get_threadDetails['thread']

	return {'err': 0, 'thread': thread}

def threadOpenOrClose(request_data, option):
	try: 
		thread_id = request_data['thread']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	if option == 'close': status = 1
	if option == 'open': status = 0

	get_cursor = Util.sendQuery("UPDATE Threads SET isClosed = %s WHERE id = %s", [status, thread_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	return {'err': 0, 'thread': {'thread': thread_id}}

def threadRemoveOrRestore(request_data, option):
	try: 
		thread_id = request_data['thread']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	if option == 'remove': status = 1
	if option == 'restore': status = 0

	get_cursor = Util.sendQuery("UPDATE Threads SET isDeleted = %s WHERE id = %s", [status, thread_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	return {'err': 0, 'thread': {'thread': thread_id}}

def threadVote(request_data):
	try: 
		thread_id = request_data['thread']
		vote = request_data['vote']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	if vote == -1: get_cursor = Util.sendQuery("UPDATE Threads SET dislikes = dislikes + 1 WHERE id = %s", [thread_id])
	if vote == 1: get_cursor = Util.sendQuery("UPDATE Threads SET likes = likes + 1 WHERE id = %s", [thread_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}

	get_threadDetails = Serv.getThreadDetailsByID(thread_id, [])
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

	get_cursor = Util.sendQuery("UPDATE Threads SET message = %s, slug = %s WHERE id = %s", [message, slug, thread_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}

	get_threadDetails = Serv.getThreadDetailsByID(thread_id, [])
	if get_threadDetails['err'] != 0: return {'err': get_threadDetails['err']}
	thread = get_threadDetails['thread']

	return {'err': 0, 'thread': thread}

def threadListPosts(request_data):
	try: 
		thread_id = request_data['thread']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}
	limit = request_data.get('limit', 10000)
	order = request_data.get('order', 'desc')
	since = request_data.get('since', '0000-00-00 00:00:00')

	list_posts = Serv.getListPosts({'field': 'thread', 'key': thread_id},
							  {'limit': limit, 'order': order, 'since': since})
	if list_posts['err'] != 0: return {'err': list_posts['err']}
	listPosts = list_posts['listPosts']

	return {'err': 0, 'listPosts': listPosts}

def threadList(request_data):
	if 'user' in request_data:
		where = {'name': 'user', 'key': request_data['user']}
	if 'forum' in request_data:
		where = {'name': 'forum', 'key': request_data['forum']}
	limit = request_data.get('limit', 10000)
	order = request_data.get('order', 'desc')
	since = request_data.get('since', '0000-00-00 00:00:00')

	list_thread = Serv.getList('Threads', where, {'limit': limit, 'order': order, 'since': since})
	if list_thread['err'] != 0: return {'err': list_thread['err']}
	listThreads = list_thread['listEntity']

	return {'err': 0, 'listEntity': listThreads}

def threadSubscribeOrUnsubscribe(request_data, option):
	try:
		user_email = request_data['user']
		thread_id = request_data['thread']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	get_user_id = Serv.getUserIDByEmail(user_email)
	if get_user_id['err'] != 0: return {'err': get_user_id['err']}
	user_id = get_user_id['user_id']

	if option == 'subscribe':
		get_cursor = Util.sendQuery("INSERT INTO Subscriptions (thread_id, user_id) VALUES (%s, %s)", [thread_id, user_id])
	if option == 'unsubscribe':
		get_cursor = Util.sendQuery("DELETE FROM Subscriptions WHERE thread_id = %s AND user_id = %s", [thread_id, user_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}

	return {'err': 0, 'subscribe': {'thread': thread_id, 'user': user_email}}

def createNewThread(data):
	get_cursor = Util.sendQuery("INSERT INTO Threads (title, date, message, slug, isClosed, isDeleted, user, forum) " +\
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
	get_cursor = Util.sendQuery("SELECT * FROM Threads WHERE user=%s AND date=%s", [data['user_id'], data['date']])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']

	if cursor.rowcount == 0: return {'err': "Thread whith user_id = " + str(data['user_id']) + " and date = " + data['date'] + " not found"}
	thread = Util.dictfetchall(cursor)[0]
	thread['date'] = thread['date'].strftime("%Y-%m-%d %H:%M:%S")
	return {'err': 0, 'thread': thread}




















