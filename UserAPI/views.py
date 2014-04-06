import json

from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import connection
from django.db import transaction

from UserAPI import dbService
from UserAPI.functions import dictfetchall, HttpResponseJSONSuccess, HttpResponseJSONFailure

@csrf_exempt
def create(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	user_create = dbService.userCreate(request_data)
	if user_create['err'] != 0: return HttpResponseJSONFailure(user_create['err'])
	user = user_create['user']

	return HttpResponseJSONSuccess(user)

def details(request):
	if request.method != 'GET' : return HttpResponseJSONFailure("Method GET is expected")

	request_data = request.GET

	user_details = dbService.userDetails(request_data)
	if user_details['err'] != 0: return HttpResponseJSONFailure(user_details['err'])
	user = user_details['user']
	
	return HttpResponseJSONSuccess(user)

def listFollowers(request):
	if request.method != 'GET' : return HttpResponseJSONFailure("Method GET is expected")

	request_data = request.GET

	user_listFollowers = dbService.userFollowList(request_data, 'followers')
	if user_listFollowers['err'] != 0: return HttpResponseJSONFailure(user_listFollowers['err'])
	followersList = user_listFollowers['followList']
	
	return HttpResponseJSONSuccess(followersList)

def listFollowing(request):
	if request.method != 'GET' : return HttpResponseJSONFailure("Method GET is expected")

	request_data = request.GET

	user_listFollowing = dbService.userFollowList(request_data, 'following')
	if user_listFollowing['err'] != 0: return HttpResponseJSONFailure(user_listFollowing['err'])
	followingList = user_listFollowing['followList']
	
	return HttpResponseJSONSuccess(followingList)