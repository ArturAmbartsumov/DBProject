import json
import requests
params = {'user': 'user5@mail.ru'}
url = 'http://127.0.0.1:8000/user/details/'
r = requests.get(url, params)
print r.status_code
#print r.text
print r.json()