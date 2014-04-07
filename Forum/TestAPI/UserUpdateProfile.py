import json
import requests
url = 'http://127.0.0.1:8000/user/updateProfile/'
payload = {'about': 'Hello im Artur', 'user': 'Artur@mail.ru', 'name': 'Artur'}
r = requests.post(url, data=json.dumps(payload))
print r.status_code
#print r.text
print r.json()