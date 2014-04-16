import datetime
import time

from django.db import IntegrityError

from Forum.dbService import service as Serv
from Forum.dbService import functions as Util

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

	get_user_id = Serv.getUserIDByEmail(user_email)
	if get_user_id['err'] != 0: return {'err': get_user_id['err']}
	user_id = get_user_id['user_id']

	get_forum_id = Serv.getForumIDByShortname(forum_short_name)
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

	get_post = Serv.getPostDetailsByID(post_id, related)
	if get_post['err'] != 0: return {'err': get_post['err']}
	post = get_post['post']

	return {'err': 0, 'post': post}

def postRemoveOrRestore(request_data, option):
	try: 
		post_id = request_data['post']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	if option == 'remove': status = 1
	if option == 'restore': status = 0

	get_cursor = Util.sendQuery("UPDATE Posts SET isDeleted = %s WHERE id = %s", [status, post_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	return {'err': 0, 'post': {'post': post_id}}

def postVote(request_data):
	try: 
		post_id = request_data['post']
		vote = request_data['vote']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	if vote == -1: get_cursor = Util.sendQuery("UPDATE Posts SET dislikes = dislikes + 1 WHERE id = %s", [post_id])
	if vote == 1: get_cursor = Util.sendQuery("UPDATE Posts SET likes = likes + 1 WHERE id = %s", [post_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}

	get_postDetails = Serv.getPostDetailsByID(post_id)
	if get_postDetails['err'] != 0: return {'err': get_postDetails['err']}
	post = get_postDetails['post']

	return {'err': 0, 'post': post}

def postUpdate(request_data):
	try:
		message = request_data['message']
		post_id = request_data['thread']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	get_cursor = Util.sendQuery("UPDATE Posts SET message = %s WHERE id = %s", [message, post_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}

	get_postDetails = Serv.getPostDetailsByID(post_id)
	if get_postDetails['err'] != 0: return {'err': get_postDetails['err']}
	post = get_postDetails['post']

	return {'err': 0, 'post': post}

def createNewPost(data):
	get_cursor = Util.sendQuery("INSERT INTO Posts (date, message, isApproved, isHighlighted, isEdited, isSpam, isDeleted, parent, user, forum, thread) " +\
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
	get_cursor = Util.sendQuery("SELECT * FROM Posts WHERE user=%s AND date=%s", [data['user_id'], data['date']])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']

	if cursor.rowcount == 0: return {'err': "Post whith user_id = " + str(data['user_id']) + " and date = " + data['date'] + " not found"}
	post = Util.dictfetchall(cursor)[0]
	post['date'] = post['date'].strftime("%Y-%m-%d %H:%M:%S")
	return {'err': 0, 'post': post}

