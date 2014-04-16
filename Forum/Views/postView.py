from django.views.decorators.csrf import csrf_exempt

from Forum.dbService.postService import *
from Forum.dbService.functions import *

@csrf_exempt
def create(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	post_create = postCreate(request_data)
	if post_create['err'] != 0: return HttpResponseJSONFailure(post_create['err'])
	post = post_create['post']

	return HttpResponseJSONSuccess(post)

def details(request):
	if request.method != 'GET' : return HttpResponseJSONFailure("Method GET is expected")

	request_data = request.GET

	post_details = postDetails(request_data)
	if post_details['err'] != 0: return HttpResponseJSONFailure(post_details['err'])
	post = post_details['post']
	
	return HttpResponseJSONSuccess(post)

def list(request):
	if request.method != 'GET' : return HttpResponseJSONFailure("Method GET is expected")

	request_data = request.GET

	post_list = postList(request_data)
	if post_list['err'] != 0: return HttpResponseJSONFailure(post_list['err'])
	posts = post_list['list']
	
	return HttpResponseJSONSuccess(posts)

@csrf_exempt
def remove(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	post_remove = postRemoveOrRestore(request_data, 'remove')
	if post_remove['err'] != 0: return HttpResponseJSONFailure(post_remove['err'])
	post = post_remove['post']

	return HttpResponseJSONSuccess(post)

@csrf_exempt
def restore(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	post_restore = postRemoveOrRestore(request_data, 'restore')
	if post_restore['err'] != 0: return HttpResponseJSONFailure(post_restore['err'])
	post = post_restore['post']

	return HttpResponseJSONSuccess(post)

@csrf_exempt
def update(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	post_update = postUpdate(request_data)
	if post_update['err'] != 0: return HttpResponseJSONFailure(post_update['err'])
	post = post_update['post']

	return HttpResponseJSONSuccess(post)

@csrf_exempt
def vote(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	post_vote = postVote(request_data)
	if post_vote['err'] != 0: return HttpResponseJSONFailure(post_vote['err'])
	post = post_vote['post']

	return HttpResponseJSONSuccess(post)














