import json
import requests
url = 'http://127.0.0.1:8000/user/create/'
payload = {'username': 'user8', 'about': 'hello im user8', 'isAnonymous': False, 'name': 'John', 'email': 'user8@mail.ru'}
r = requests.post(url, data=json.dumps(payload))
print r.status_code
#print r.text
print r.json()