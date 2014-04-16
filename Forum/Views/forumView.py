from django.views.decorators.csrf import csrf_exempt

from Forum.dbService.forumService import *
from Forum.dbService.functions import *

@csrf_exempt
def create(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	forum_create = forumCreate(request_data)
	if forum_create['err'] != 0: return HttpResponseJSONFailure(forum_create['err'])
	forum = forum_create['forum']

	return HttpResponseJSONSuccess(forum)

def details(request):
	if request.method != 'GET' : return HttpResponseJSONFailure("Method GET is expected")

	request_data = request.GET

	forum_details = forumDetails(request_data)
	if forum_details['err'] != 0: return HttpResponseJSONFailure(forum_details['err'])
	forum = forum_details['forum']
	
	return HttpResponseJSONSuccess(forum)

def listPosts(request):
	if request.method != 'GET' : return HttpResponseJSONFailure("Method GET is expected")

	request_data = request.GET

	forum_listPosts = forumListPosts(request_data)
	if forum_listPosts['err'] != 0: return HttpResponseJSONFailure(forum_listPosts['err'])
	listPosts = forum_listPosts['listPosts']
	
	return HttpResponseJSONSuccess(listPosts)