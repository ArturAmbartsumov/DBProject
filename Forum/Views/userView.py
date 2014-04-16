from django.views.decorators.csrf import csrf_exempt

from Forum.dbService.userService import *
from Forum.dbService.functions import *

@csrf_exempt
def create(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	user_create = userCreate(request_data)
	if user_create['err'] != 0: return HttpResponseJSONFailure(user_create['err'])
	user = user_create['user']

	return HttpResponseJSONSuccess(user)

def details(request):
	if request.method != 'GET' : return HttpResponseJSONFailure("Method GET is expected")

	request_data = request.GET

	user_details = userDetails(request_data)
	if user_details['err'] != 0: return HttpResponseJSONFailure(user_details['err'])
	user = user_details['user']
	
	return HttpResponseJSONSuccess(user)

def listFollowers(request):
	if request.method != 'GET' : return HttpResponseJSONFailure("Method GET is expected")

	request_data = request.GET

	user_listFollowers = userFollowList(request_data, 'followers')
	if user_listFollowers['err'] != 0: return HttpResponseJSONFailure(user_listFollowers['err'])
	followersList = user_listFollowers['followList']
	
	return HttpResponseJSONSuccess(followersList)

def listFollowing(request):
	if request.method != 'GET' : return HttpResponseJSONFailure("Method GET is expected")

	request_data = request.GET

	user_listFollowing = userFollowList(request_data, 'following')
	if user_listFollowing['err'] != 0: return HttpResponseJSONFailure(user_listFollowing['err'])
	followingList = user_listFollowing['followList']
	
	return HttpResponseJSONSuccess(followingList)

def listPosts(request):
	if request.method != 'GET' : return HttpResponseJSONFailure("Method GET is expected")

	request_data = request.GET

	user_listPosts = userListPosts(request_data)
	if user_listPosts['err'] != 0: return HttpResponseJSONFailure(user_listPosts['err'])
	listPosts = user_listPosts['listPosts']
	
	return HttpResponseJSONSuccess(listPosts)

@csrf_exempt
def follow(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")
	
	request_data = json.loads(request.body)

	user_follow = userFollow(request_data, 'set')
	if user_follow['err'] != 0: return HttpResponseJSONFailure(user_follow['err'])
	user = user_follow['user']
	
	return HttpResponseJSONSuccess(user)

@csrf_exempt
def unfollow(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")
	
	request_data = json.loads(request.body)

	user_follow = userFollow(request_data, 'drop')
	if user_follow['err'] != 0: return HttpResponseJSONFailure(user_follow['err'])
	user = user_follow['user']
	
	return HttpResponseJSONSuccess(user)

@csrf_exempt
def updateProfile(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")
	
	request_data = json.loads(request.body)

	user_update = userUpdateProfile(request_data)
	if user_update['err'] != 0: return HttpResponseJSONFailure(user_update['err'])
	user = user_update['user']
	
	return HttpResponseJSONSuccess(user)
	
