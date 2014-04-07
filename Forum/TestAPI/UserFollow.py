import json
import requests
url = 'http://127.0.0.1:8000/user/unfollow/'
payload = {'follower': 'user5@mail.ru'}
r = requests.post(url, data=json.dumps(payload))
print r.status_code
#print r.text
print r.json()