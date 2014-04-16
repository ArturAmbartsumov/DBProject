from django.views.decorators.csrf import csrf_exempt

from Forum.dbService.threadService import *
from Forum.dbService.functions import *

@csrf_exempt
def create(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	thread_create = threadCreate(request_data)
	if thread_create['err'] != 0: return HttpResponseJSONFailure(thread_create['err'])
	thread = thread_create['thread']

	return HttpResponseJSONSuccess(thread)

def details(request):
	if request.method != 'GET' : return HttpResponseJSONFailure("Method GET is expected")

	request_data = request.GET

	thread_details = threadDetails(request_data)
	if thread_details['err'] != 0: return HttpResponseJSONFailure(thread_details['err'])
	thread = thread_details['thread']
	
	return HttpResponseJSONSuccess(thread)

@csrf_exempt
def close(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	thread_close = threadOpenOrClose(request_data, 'close')
	if thread_close['err'] != 0: return HttpResponseJSONFailure(thread_close['err'])
	thread = thread_close['thread']

	return HttpResponseJSONSuccess(thread)

@csrf_exempt
def open(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	thread_open = threadOpenOrClose(request_data, 'open')
	if thread_open['err'] != 0: return HttpResponseJSONFailure(thread_open['err'])
	thread = thread_open['thread']

	return HttpResponseJSONSuccess(thread)

def list(request):
	if request.method != 'GET' : return HttpResponseJSONFailure("Method GET is expected")

	request_data = request.GET

	thread_list = threadList(request_data)
	if thread_list['err'] != 0: return HttpResponseJSONFailure(thread_list['err'])
	threads = thread_list['list']
	
	return HttpResponseJSONSuccess(threads)

def listPosts(request):
	if request.method != 'GET' : return HttpResponseJSONFailure("Method GET is expected")

	request_data = request.GET

	thread_listPosts = threadListPosts(request_data)
	if thread_listPosts['err'] != 0: return HttpResponseJSONFailure(thread_listPosts['err'])
	listPosts = thread_listPosts['listPosts']
	
	return HttpResponseJSONSuccess(listPosts)

@csrf_exempt
def remove(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	thread_remove = threadRemoveOrRestore(request_data, 'remove')
	if thread_remove['err'] != 0: return HttpResponseJSONFailure(thread_remove['err'])
	thread = thread_remove['thread']

	return HttpResponseJSONSuccess(thread)

@csrf_exempt
def restore(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	thread_restore = threadRemoveOrRestore(request_data, 'restore')
	if thread_restore['err'] != 0: return HttpResponseJSONFailure(thread_restore['err'])
	thread = thread_restore['thread']

	return HttpResponseJSONSuccess(thread)

@csrf_exempt
def subscribe(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	thread_subscribe = threadSubscribeOrUnsubscribe(request_data, 'subscribe')
	if thread_subscribe['err'] != 0: return HttpResponseJSONFailure(thread_subscribe['err'])
	subscribe = thread_subscribe['subscribe']

	return HttpResponseJSONSuccess(subscribe)

@csrf_exempt
def unsubscribe(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	thread_unsubscribe = threadSubscribeOrUnsubscribe(request_data, 'unsubscribe')
	if thread_unsubscribe['err'] != 0: return HttpResponseJSONFailure(thread_unsubscribe['err'])
	unsubscribe = thread_unsubscribe['subscribe']

	return HttpResponseJSONSuccess(unsubscribe)

@csrf_exempt
def update(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	thread_update = threadUpdate(request_data)
	if thread_update['err'] != 0: return HttpResponseJSONFailure(thread_update['err'])
	thread = thread_update['thread']

	return HttpResponseJSONSuccess(thread)

@csrf_exempt
def vote(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")

	request_data = json.loads(request.body)

	thread_vote = threadVote(request_data)
	if thread_vote['err'] != 0: return HttpResponseJSONFailure(thread_vote['err'])
	thread = thread_vote['thread']

	return HttpResponseJSONSuccess(thread)











