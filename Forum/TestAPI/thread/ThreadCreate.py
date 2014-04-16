import json
import requests
import datetime
url = 'http://127.0.0.1:8000/thread/create/'
payload = {'forum': 'forum_3',
		   'title': 'Tred 7',
		   'isClosed': False,
		   'user': 'user4@mail.ru',
		   'date': (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
		   'message': 'messageTred7',
		   'slug': 'tred_7',
		   'isDeleted': False}
r = requests.post(url, data=json.dumps(payload))
print r.status_code
#print r.text
print r.json()