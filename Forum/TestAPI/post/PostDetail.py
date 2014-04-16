import json
import requests
payload = {'related': ['user', 'forum', 'thread'], 'post': '6'}
url = 'http://127.0.0.1:8000/post/details/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()