import json
import requests
payload = {'related': ['thread'],
		   'since': '2014-01-02 00:00:00',
		   'limit': 2, 'order': 'asc',
		   'forum': 'forum_5'}
url = 'http://127.0.0.1:8000/forum/listPosts/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()