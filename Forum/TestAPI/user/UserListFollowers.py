import json
import requests
payload = {'user': 'user3@mail.ru', 'order': 'asc'}
url = 'http://127.0.0.1:8000/user/listFollowers/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()