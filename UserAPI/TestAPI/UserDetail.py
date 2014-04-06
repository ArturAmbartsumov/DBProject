import json
import requests
payload = {'user': 'use@mail.ru'}
url = 'http://127.0.0.1:8000/user/details/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()