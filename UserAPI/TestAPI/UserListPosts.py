import json
import requests
url = 'http://127.0.0.1:8000/user/details/?user=art@mail.ru'
r = requests.get(url)
print r.status_code
print r.text
print r.json()