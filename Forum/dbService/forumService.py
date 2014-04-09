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

	get_id = getIDByEmail(email)
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
	related = request_data.get('related', [])

	get_forum = getForum(short_name)
	if get_forum['err'] != 0: return {'err': get_forum['err']}
	forum = get_forum['forum']

	if 'user' in related:
		get_user = getUserDetailsById(forum['user'])
		if get_user['err'] != 0: return {'err': get_user['err']}
		user = get_user['user']
	else:
		get_user = getEmailByID(forum['user'])
		if get_user['err'] != 0: return {'err': get_user['err']}
		user = get_user['email']

	forum['user'] = user
	return {'err': 0, 'forum': forum}


def createNewForum(data):
	get_cursor = sendQuery("INSERT INTO Forums (name, short_name, user) " +\
						   "VALUES (%s, %s, %s)",
						   [data['name'], data['short_name'], data['user']])
	if get_cursor['err'] != 0: return {'err': get_user['err']}
	cursor = get_cursor['cursor']
	return {'err': 0}

def getForum(short_name):
	get_cursor = sendQuery("SELECT * FROM Forums WHERE short_name=%s", [short_name])
	if get_cursor['err'] != 0: return {'err': get_user['err']}
	cursor = get_cursor['cursor']

	if cursor.rowcount != 1: return {'err': "Forum whith short_name = " + short_name + " not found"}
	return {'err': 0, 'forum': dictfetchall(cursor)[0]}

