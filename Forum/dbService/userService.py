import json

from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import connection
from django.db import transaction

from Forum.dbService.functions import *
from Forum.dbService.postService import *

def userCreate(request_data):
	try: 
		username = request_data['username']
		about = request_data['about']
		name = request_data['name']
		email = request_data['email']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}
	isAnonymous = request_data.get('isAnonymous', False)

	get_cursor = sendQuery("INSERT INTO Users (username, email, name, about, isAnonymous)" +\
						   "VALUES (%s, %s, %s, %s, %s)", [username, email, name, about, isAnonymous])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	
	get_user = getUser(email)
	if get_user['err'] != 0: return {'err': get_user['err']}
	user = get_user['user']

	return {'err': 0, 'user': user}

def userDetails(request_data):
	try:
		email = request_data['user']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	get_user = getUser(email)
	if get_user['err'] != 0: return {'err': get_user['err']}
	user = get_user['user']

	get_fullUser = buildFullUserDetails(user)
	if get_fullUser['err'] != 0: return {'err': get_fullUser['err']}
	fullUser = get_fullUser['user']

	return {'err': 0, 'user': fullUser}

def userFollow(request_data, dropOrSet):
	try:
		emailFollower = request_data['follower']
		emailFollowee = request_data['followee']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	get_Follower = getUser(emailFollower)
	if get_Follower['err'] != 0: return {'err': get_Follower['err']}
	user = get_Follower['user']

	get_FolloweeID = getUserIDByEmail(emailFollowee)
	if get_FolloweeID['err'] != 0: return {'err': get_FolloweeID['err']}
	followeeID = get_FolloweeID['user_id']

	if dropOrSet == 'set': err = setFollow(user['id'], followeeID)
	if dropOrSet == 'drop': err = dropFollow(user['id'], followeeID)
	if err['err'] != 0: return {'err': err['err']}

	get_fullUser = buildFullUserDetails(user)
	if get_fullUser['err'] != 0: return {'err': get_fullUser['err']}
	fullUser = get_fullUser['user']

	return {'err': 0, 'user': fullUser}

def userUpdateProfile(request_data):
	try:
		about = request_data['about']
		email = request_data['user']
		name = request_data['name']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}

	err = updateUser({'name': name, 'about': about, 'email': email})
	if err['err'] != 0: return {'err': err['err']}

	user_details = userDetails({'user': email})
	if user_details['err'] != 0: return {'err': user_details['err']}
	user = user_details['user']

	return {'err': 0, 'user': user}

def updateUser(data):
	get_cursor = sendQuery("UPDATE Users SET name = %s, about = %s " +\
						   "WHERE email = %s", [data['name'], data['about'], data['email']])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']

	return {'err': 0}

def userFollowList(request_data, followersOrFollowing):
	try: 
		email = request_data['user']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}
	limit = request_data.get('limit', 10000)
	order = request_data.get('order', 'desc')
	since_id = request_data.get('since_id', 0)

	get_id = getUserIDByEmail(email)
	if get_id['err'] != 0: return {'err': get_id['err']}
	user_id = get_id['user_id']

	data = {'user_id': user_id, 'limit': limit, 'order': order, 'since_id': since_id}
	
	if followersOrFollowing == 'followers': get_follow = getFollowers(data)
	if followersOrFollowing == 'following': get_follow = getFollowing(data)
	if get_follow['err'] != 0: return {'err': get_follow['err']}
	followList = get_follow['followList']
	
	for user in followList:
		get_fullUser = buildFullUserDetails(user)
		if get_fullUser['err'] != 0: return {'err': get_fullUser['err']}
		user = get_fullUser['user']

	return {'err': 0, 'followList': followList}

def userListPosts(request_data):
	try: 
		user_email = request_data['user']
	except KeyError as e:
		return {'err': str(e) + ' argument not found'}
	limit = request_data.get('limit', 10000)
	order = request_data.get('order', 'desc')
	since = request_data.get('since', '0000-00-00 00:00:00')

	list_posts = getListPosts({'field': 'user_email', 'key': user_email},
							  {'limit': limit, 'order': order, 'since': since})
	if list_posts['err'] != 0: return {'err': list_posts['err']}
	listPosts = list_posts['listPosts']
	return {'err': 0, 'listPosts': listPosts}



def getFollowers(data):
	get_cursor = sendQuery("SELECT id, username, email, name, about, isAnonymous " +\
						   "FROM Users, (" +\
						       "SELECT follower_id FROM Followers WHERE user_id = %s AND follower_id >= %s" +\
						   ") AS T " +\
						   "WHERE Users.id = T.follower_id " +\
						   "ORDER BY Users.name " + data['order'] +\
						   " LIMIT %s", [data['user_id'], data['since_id'], data['limit']])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	return {'err': 0, 'followList': dictfetchall(cursor)}

def getFollowing(data):
	get_cursor = sendQuery("SELECT id, username, email, name, about, isAnonymous " +\
						   "FROM Users, (" +\
						       "SELECT follower_id FROM Followers WHERE user_id = %s AND follower_id >= %s" +\
						   ") AS T " +\
						   "WHERE Users.id = T.follower_id " +\
						   "ORDER BY Users.name " + data['order'] +\
						   " LIMIT %s", [data['user_id'], data['since_id'], data['limit']])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	return {'err': 0, 'followList': dictfetchall(cursor)}

def getFollowersEmails(user_id):
	get_cursor = sendQuery("SELECT Users.email AS emails FROM Users, " +\
						   "(SELECT follower_id FROM Followers WHERE user_id = %s) AS T " +\
						   "WHERE Users.id = T.follower_id", [user_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	return {'err': 0, 'followers': transformToList(cursor.fetchall())}

def getFollowingEmails(user_id):
	get_cursor = sendQuery("SELECT Users.email AS emails FROM Users, " +\
						   "(SELECT user_id FROM Followers WHERE follower_id = %s) AS T " +\
						   "WHERE Users.id = T.user_id", [user_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	return {'err': 0, 'followers': transformToList(cursor.fetchall())}	

def getSubscriptionsID(user_id):
	get_cursor = sendQuery("SELECT thread_id FROM Subscriptions WHERE user_id = %s", [user_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	return {'err': 0, 'subscriptions': transformToList(cursor.fetchall())}

def setFollow(follower_id, followee_id):
	get_cursor = sendQuery("INSERT INTO Followers (user_id, follower_id)" +\
						   "VALUES (%s, %s)", [followee_id, follower_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	
	return {'err': 0}

def dropFollow(follower_id, followee_id):
	get_cursor = sendQuery("DELETE FROM Followers " +\
						   "WHERE user_id = %s AND follower_id = %s", [followee_id, follower_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	
	if cursor.rowcount == 0: return {'err': 'Follow not found'}
	return {'err': 0}

def getUserIDByEmail(email):
	get_cursor = sendQuery("SELECT id FROM Users WHERE email = %s", [email])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	
	if cursor.rowcount != 1: return {'err': "User whith email = " + email + " not found"}
	users_id = transformToList(cursor.fetchall())
	return {'err': 0, 'user_id': users_id[0]}

def getUserEmailByID(user_id):
	get_cursor = sendQuery("SELECT email FROM Users WHERE id = %s", [user_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	
	if cursor.rowcount != 1: return {'err': "User whith ID = " + str(user_id) + " not found"}
	email = transformToList(cursor.fetchall())
	return {'err': 0, 'email': email[0]}

def getUser(email):
	get_cursor = sendQuery("SELECT * FROM Users WHERE email=%s", [email])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	
	if cursor.rowcount != 1: return {'err': "User whith email = " + email + " not found"}
	return {'err': 0, 'user': dictfetchall(cursor)[0]}

def getUserById(user_id):
	get_cursor = sendQuery("SELECT * FROM Users WHERE id=%s", [user_id])
	if get_cursor['err'] != 0: return {'err': get_cursor['err']}
	cursor = get_cursor['cursor']
	
	if cursor.rowcount != 1: return {'err': "User whith ID = " + str(user_id) + " not found"}
	return {'err': 0, 'user': dictfetchall(cursor)[0]}

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




























