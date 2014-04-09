import json
import requests
url = 'http://127.0.0.1:8000/forum/create/'
payload = {'name': 'Forum 6', 'short_name': 'forum_6', 'user': 'user2@mail.ru'}
r = requests.post(url, data=json.dumps(payload))
print r.status_code
#print r.text
print r.json()