from django.db import IntegrityError

from Forum.dbService import service as Serv
from Forum.dbService import functions as Util

def forumCreate(request_data):
	try: 
		short_name = request_data['short_name']
		name = request_data['name']
		email = request_data['user']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	get_id = Serv.getUserIDByEmail(email)
	if get_id['err'] != 0: return {'err': get_id['err']}
	user_id = get_id['user_id']

	err = createNewForum({'short_name': short_name, 'name': name, 'user': user_id})
	if err['err'] != 0: return {'err': err['err']}

	get_forum = getForum(short_name)
	if get_forum['err'] != 0: return {'err': get_forum['err']}
	forum = get_forum['forum']

	forum['user'] = email

	return {'err': 0, 'forum': forum}

def forumDetails(request_data):
	try: 
		short_name = request_data['forum']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}
	related = request_data.getlist('related', [])

	get_forum = getForum(short_name)
	if get_forum['err'] != 0: return {'err': get_forum['err']}
	forum = get_forum['forum']

	if 'user' in related:
		get_user = Serv.getUserDetailsById(forum['user'])
		if get_user['err'] != 0: return {'err': get_user['err']}
		user = get_user['user']
	else:
		get_user = Serv.getUserEmailByID(forum['user'])
		if get_user['err'] != 0: return {'err': get_user['err']}
		user = get_user['email']

	forum['user'] = user
	return {'err': 0, 'forum': forum}

def forumListPosts(request_data):
	try: 
		forum_short_name = request_data['forum']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}
	related = request_data.getlist('related', [])
	limit = request_data.get('limit', 10000)
	order = request_data.get('order', 'desc')
	since = request_data.get('since', '0000-00-00 00:00:00')

	list_posts = Serv.getListPostsInForum(forum_short_name, related, {'limit': limit, 'order': order, 'since': since})
	if list_posts['err'] != 0: return {'err': list_posts['err']}
	listPosts = list_posts['listPosts']
	return {'err': 0, 'listPosts': listPosts}


def createNewForum(data):
	get_cursor = Util.sendQuery("INSERT INTO Forums (name, short_name, user) " +\
						   "VALUES (%s, %s, %s)",
						   [data['name'], data['short_name'], data['user']])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	return {'err': 0}

def getForum(short_name):
	get_cursor = Util.sendQuery("SELECT * FROM Forums WHERE short_name=%s", [short_name])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']

	if cursor.rowcount != 1: return {'err': "Forum whith short_name = " + short_name + " not found"}
	return {'err': 0, 'forum': Util.dictfetchall(cursor)[0]}



















