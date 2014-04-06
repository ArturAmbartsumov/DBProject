import json

from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import connection
from django.db import transaction
from UserAPI.functions import dictfetchall, HttpResponseJSONSuccess, HttpResponseJSONFailure

def userCreate(request_data):
	try: 
		username = request_data['username']
		about = request_data['about']
		name = request_data['name']
		email = request_data['email']
	except KeyError as e:
		return {'err': str(e)}
	isAnonymous = request_data.get('isAnonymous', False)

	cursor = connection.cursor()
	try:
		with transaction.atomic():
			cursor.execute("INSERT INTO Users (username, email, name, about, isAnonymous)" +\
						   "VALUES (%s, %s, %s, %s, %s)", [username, email, name, about, isAnonymous])
	except IntegrityError as e:
		return {'err': str(e)}
	
	get_user = getUser(email)
	if get_user['err'] != 0: return {'err': get_user['err']}
	user = get_user['user']

	return {'err': 0, 'user': user}

def userDetails(request_data):
	try:
		email = request_data['user']
	except KeyError as e:
		return {'err': str(e)}

	get_user = getUser(email)
	if get_user['err'] != 0: return {'err': get_user['err']}
	user = get_user['user']

	get_followers = getFollowers(user['id'])
	if get_followers['err'] != 0: return {'err': get_followers['err']}
	followers = get_followers['followers']

	get_following = getFollowing(user['id'])
	if get_following['err'] != 0: return {'err': get_following['err']}
	following = get_following['followers']

	get_subscriptions = getSubscriptions(user['id'])
	if get_subscriptions['err'] != 0: return {'err': get_subscriptions['err']}
	subscriptions = get_subscriptions['subscriptions']

	user['followers'] = followers
	user['following'] = following
	user['subscriptions'] = subscriptions

	return {'err': 0, 'user': user}

def getUser(email):
	cursor = connection.cursor()
	try:
		with transaction.atomic():
			cursor.execute("SELECT * FROM Users WHERE email=%s", [email])
	except IntegrityError as e:
		return {'err': str(e)}
	return {'err': 0, 'user': dictfetchall(cursor)[0]}

def getFollowers(user_id):
	cursor = connection.cursor()
	#get_id = getIDByEmail(email)
	#if get_id['err'] != 0: return {'err': get_id['err']}
	#user_id = get_id['user_id']
	try:
		with transaction.atomic():
			cursor.execute("SELECT Users.email AS emails FROM Users, " +\
						   "(SELECT follower_id FROM Followers WHERE user_id = %s) AS T " +\
						   "WHERE Users.id = T.follower_id", [user_id])
	except IntegrityError as e:
		return {'err': str(e)}
	return {'err': 0, 'followers': dictfetchall(cursor)}

def getFollowing(user_id):
	cursor = connection.cursor()
	#get_id = getIDByEmail(email)
	#if get_id['err'] != 0: return {'err': get_id['err']}
	#user_id = get_id['user_id']
	try:
		with transaction.atomic():
			cursor.execute("SELECT Users.email AS emails FROM Users, " +\
						   "(SELECT user_id FROM Followers WHERE follower_id = %s) AS T " +\
						   "WHERE Users.id = T.user_id", [user_id])
	except IntegrityError as e:
		return {'err': str(e)}
	return {'err': 0, 'followers': dictfetchall(cursor)}	

def getSubscriptions(user_id):
	cursor = connection.cursor()
	try:
		with transaction.atomic():
			cursor.execute("SELECT thread_id FROM Subscriptions WHERE user_id = %s", [user_id])
	except IntegrityError as e:
		return {'err': str(e)}
	return {'err': 0, 'subscriptions': dictfetchall(cursor)}

def getIDByEmail(email):
	cursor = connection.cursor()
	try:
		with transaction.atomic():
			cursor.execute("SELECT id FROM Users WHERE email = %s", [email])
	except IntegrityError as e:
		return {'err': str(e)}
	return {'err': 0, 'user_id': dictfetchall(cursor)[0]}



















