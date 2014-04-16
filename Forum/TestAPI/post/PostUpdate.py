import json
import requests
import datetime
url = 'http://127.0.0.1:8000/post/update/'
payload =  {'message': 'hey hey hey hey!', 'thread': 6}
r = requests.post(url, data=json.dumps(payload))
print r.status_code
#print r.text
print r.json()