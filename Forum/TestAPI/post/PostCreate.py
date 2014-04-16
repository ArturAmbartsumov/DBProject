import json
import requests
import datetime
url = 'http://127.0.0.1:8000/post/create/'
payload = {'isApproved': True,
		   'user': 'user5@mail.ru',
		   'date': (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
		   'message': 'message post 1',
		   'isSpam': False,
		   'isHighlighted': True,
		   'thread': 23,
		   'forum': 'forum_5',
		   'isDeleted': False,
		   'isEdited': True,
		   'parent': 7}
r = requests.post(url, data=json.dumps(payload))
print r.status_code
#print r.text
print r.json()