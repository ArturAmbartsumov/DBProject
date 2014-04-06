import json

from django.http import HttpResponse
from django.db import connection
from django.db import transaction

def dictfetchall(cursor):
	desc = cursor.description
	arr = [
		dict(zip([col[0] for col in desc], row))
		for row in cursor.fetchall()
	]
	return arr

def HttpResponseJSONSuccess(response_data):
	r = {'code' : 0, 'response' : response_data}
	return HttpResponse(json.dumps(r), content_type="javascript/json")

def HttpResponseJSONFailure(response_data):
	r = {'code' : 1, 'response' : response_data}
	return HttpResponse(json.dumps(r), content_type="javascript/json")