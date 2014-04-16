import json

from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import connection
from django.db import transaction

from Forum.dbService.userService import *
from Forum.dbService.functions import *

def forumCreate(request_data):
	try: 
		short_name = request_data['short_name']
		name = request_data['name']
		email = request_data['user']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	get_id = getUserIDByEmail(email)
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
		get_user = getUserDetailsById(forum['user'])
		if get_user['err'] != 0: return {'err': get_user['err']}
		user = get_user['user']
	else:
		get_user = getUserEmailByID(forum['user'])
		if get_user['err'] != 0: return {'err': get_user['err']}
		user = get_user['email']

	forum['user'] = user
	return {'err': 0, 'forum': forum}

def createNewForum(data):
	get_cursor = sendQuery("INSERT INTO Forums (name, short_name, user) " +\
						   "VALUES (%s, %s, %s)",
						   [data['name'], data['short_name'], data['user']])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	return {'err': 0}

def getForumDetailsById(forum_id):
	get_forum = getForumByID(forum_id)
	if get_forum['err'] != 0: return {'err': get_forum['err']}
	forum = get_forum['forum']

	get_user = getUserEmailByID(forum['user'])
	if get_user['err'] != 0: return {'err': get_user['err']}
	user = get_user['email']

	forum['user'] = user
	return {'err': 0, 'forum': forum}


def getForum(short_name):
	get_cursor = sendQuery("SELECT * FROM Forums WHERE short_name=%s", [short_name])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']

	if cursor.rowcount != 1: return {'err': "Forum whith short_name = " + short_name + " not found"}
	return {'err': 0, 'forum': dictfetchall(cursor)[0]}

def getForumByID(forum_id):
	get_cursor = sendQuery("SELECT * FROM Forums WHERE id=%s", [forum_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']

	if cursor.rowcount != 1: return {'err': "Forum whith id = " + str(forum_id) + " not found"}
	return {'err': 0, 'forum': dictfetchall(cursor)[0]}

def getForumIDByShortname(short_name):
	get_cursor = sendQuery("SELECT id FROM Forums WHERE short_name = %s", [short_name])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	
	if cursor.rowcount != 1: return {'err': "Forum whith short_name = " + short_name + " not found"}
	forum_id = transformToList(cursor.fetchall())
	return {'err': 0, 'forum_id': forum_id[0]}

def getShortnameByForumID(forum_id):
	get_cursor = sendQuery("SELECT short_name FROM Forums WHERE id = %s", [forum_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	
	if cursor.rowcount != 1: return {'err': "Forum whith id = " + str(forum_id) + " not found"}
	short_name = transformToList(cursor.fetchall())
	return {'err': 0, 'short_name': short_name[0]}


















