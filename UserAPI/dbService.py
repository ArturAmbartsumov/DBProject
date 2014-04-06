import json

from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import connection
from django.db import transaction
from UserAPI.functions import dictfetchall, HttpResponseJSONSuccess, HttpResponseJSONFailure, transformToList

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

def userFollowList(request_data, followersOrFollowing):
	try: 
		email = request_data['user']
	except KeyError as e:
		return {'err': str(e)}
	limit = request_data.get('limit', 10000)
	order = request_data.get('order', 'desc')
	since_id = request_data.get('since_id', 0)

	get_id = getIDByEmail(email)
	if get_id['err'] != 0: return {'err': get_id['err']}
	user_id = get_id['user_id']

	data = {'user_id': user_id, 'limit': limit, 'order': order, 'since_id': since_id}
	
	if followersOrFollowing == 'followers': get_follow = getFollowers(data)
	if followersOrFollowing == 'following': get_follow = getFollowing(data)
	if get_follow['err'] != 0: return {'err': get_follow['err']}
	followList = get_follow['followList']
	
	for user in followList:
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

	return {'err': 0, 'followList': followList}


def getFollowers(data):
	cursor = connection.cursor()
	try:
		with transaction.atomic():
			if data['order'] == 'desc':
				cursor.execute("SELECT id, username, email, name, about, isAnonymous " +\
							   "FROM Users, (" +\
							       "SELECT follower_id FROM Followers WHERE user_id = %s AND follower_id >= %s" +\
							   ") AS T " +\
							   "WHERE Users.id = T.follower_id " +\
							   "ORDER BY Users.name desc " +\
							   "LIMIT %s", [data['user_id'], data['since_id'], data['limit']])
			if data['order'] == 'asc':
				cursor.execute("SELECT id, username, email, name, about, isAnonymous " +\
							   "FROM Users, (" +\
							       "SELECT follower_id FROM Followers WHERE user_id = %s AND follower_id >= %s" +\
							   ") AS T " +\
							   "WHERE Users.id = T.follower_id " +\
							   "ORDER BY Users.name asc " +\
							   "LIMIT %s", [data['user_id'], data['since_id'], data['limit']])
	except IntegrityError as e:
		return {'err': str(e)}
	return {'err': 0, 'followList': dictfetchall(cursor)}

def getFollowing(data):
	cursor = connection.cursor()
	try:
		with transaction.atomic():
			if data['order'] == 'desc':
				cursor.execute("SELECT id, username, email, name, about, isAnonymous " +\
							   "FROM Users, (" +\
							       "SELECT user_id FROM Followers WHERE follower_id = %s AND user_id >= %s" +\
							   ") AS T " +\
							   "WHERE Users.id = T.user_id " +\
							   "ORDER BY Users.name desc " +\
							   "LIMIT %s", [data['user_id'], data['since_id'], data['limit']])
			if data['order'] == 'asc':
				cursor.execute("SELECT id, username, email, name, about, isAnonymous " +\
							   "FROM Users, (" +\
							       "SELECT follower_id FROM Followers WHERE user_id = %s AND follower_id >= %s" +\
							   ") AS T " +\
							   "WHERE Users.id = T.follower_id " +\
							   "ORDER BY Users.name asc " +\
							   "LIMIT %s", [data['user_id'], data['since_id'], data['limit']])
	except IntegrityError as e:
		return {'err': str(e)}
	return {'err': 0, 'followList': dictfetchall(cursor)}

def getFollowersEmails(user_id):
	cursor = connection.cursor()
	try:
		with transaction.atomic():
			cursor.execute("SELECT Users.email AS emails FROM Users, " +\
						   "(SELECT follower_id FROM Followers WHERE user_id = %s) AS T " +\
						   "WHERE Users.id = T.follower_id", [user_id])
	except IntegrityError as e:
		return {'err': str(e)}
	return {'err': 0, 'followers': transformToList(cursor.fetchall())}

def getFollowingEmails(user_id):
	cursor = connection.cursor()
	try:
		with transaction.atomic():
			cursor.execute("SELECT Users.email AS emails FROM Users, " +\
						   "(SELECT user_id FROM Followers WHERE follower_id = %s) AS T " +\
						   "WHERE Users.id = T.user_id", [user_id])
	except IntegrityError as e:
		return {'err': str(e)}
	return {'err': 0, 'followers': transformToList(cursor.fetchall())}	

def getSubscriptionsID(user_id):
	cursor = connection.cursor()
	try:
		with transaction.atomic():
			cursor.execute("SELECT thread_id FROM Subscriptions WHERE user_id = %s", [user_id])
	except IntegrityError as e:
		return {'err': str(e)}
	return {'err': 0, 'subscriptions': transformToList(cursor.fetchall())}

def getIDByEmail(email):
	cursor = connection.cursor()
	try:
		with transaction.atomic():
			cursor.execute("SELECT id FROM Users WHERE email = %s", [email])
	except IntegrityError as e:
		return {'err': str(e)}
	if cursor.rowcount != 1: return {'err': "User whith email = " + email + " not found"}
	users_id = transformToList(cursor.fetchall())
	return {'err': 0, 'user_id': users_id[0]}

def getUser(email):
	cursor = connection.cursor()
	try:
		with transaction.atomic():
			cursor.execute("SELECT * FROM Users WHERE email=%s", [email])
	except IntegrityError as e:
		return {'err': str(e)}
	if cursor.rowcount != 1: return {'err': "User whith email = " + email + " not found"}
	return {'err': 0, 'user': dictfetchall(cursor)[0]}


















