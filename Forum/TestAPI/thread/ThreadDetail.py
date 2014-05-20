import json
import requests
payload = {'related': ['user', 'forum'], 'thread': '2'}
url = 'http://127.0.0.1:8000/db/api/thread/list/?since=2014-01-01+00%3A00%3A00&user=example2%40mail.ru&order=desc'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()