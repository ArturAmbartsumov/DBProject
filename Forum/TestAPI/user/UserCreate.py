import json
import requests
url = 'http://195.19.44.156/db/api/user/create/'
payload = {'username': 'sdfg', 'about': 'hdf', 'isAnonymous': False, 'name': 'sdf', 'email': 'Artur@mail.ru'}
r = requests.post(url, data=json.dumps(payload))
print r.status_code
#print r.text
print r.json()