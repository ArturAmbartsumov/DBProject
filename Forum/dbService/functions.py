import json

from django.db import IntegrityError
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

def transformToList(result):
	b = []
	for a in result:
		b.append(a[0])
	return b


def HttpResponseJSONSuccess(response_data):
	r = {'code' : 0, 'response' : response_data}
	return HttpResponse(json.dumps(r), content_type="javascript/json")

def HttpResponseJSONFailure(response_data):
	r = {'code' : 1, 'response' : response_data}
	return HttpResponse(json.dumps(r), content_type="javascript/json")

def sendQuery(query, arg):
	cursor = connection.cursor()
	try:
		with transaction.atomic():
			cursor.execute(query, arg)
	except IntegrityError as e:
		return {'err': str(e)}
	return {'err': 0, 'cursor': cursor}

#date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")