import json
import requests
import datetime

url = 'http://127.0.0.1:8000/db/api/clear'
r = requests.post(url)
print r.status_code
#print r.text
print r.json()

















