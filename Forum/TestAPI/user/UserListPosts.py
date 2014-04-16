import json
import requests
payload = {'user': 'user5@mail.ru', 'order': 'asc', 'since': '2014-04-14 21:27:34'}
url = 'http://127.0.0.1:8000/user/listPosts/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()