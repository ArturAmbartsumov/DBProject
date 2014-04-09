import json
import requests
payload = {'forum': 'forum_3'}
url = 'http://127.0.0.1:8000/forum/details/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()