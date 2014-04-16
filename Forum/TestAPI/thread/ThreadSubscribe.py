import json
import requests
import datetime
url = 'http://127.0.0.1:8000/thread/subscribe/'
payload =  {'user': 'user6@mail.ru', 'thread': 29}
r = requests.post(url, data=json.dumps(payload))
print r.status_code
#print r.text
print r.json()