import json
import requests
payload = {'related': ['thread', 'forum'], 'since': '2014-01-01 00:00:00', 'order': 'desc', 'forum': 'forum1'}
url = 'http://127.0.0.1:8000/db/api/forum/listPosts/?related=%5B%27thread%27%2C+%27forum%27%5D&since=2014-01-01+00%3A00%3A00&order=desc&forum=forum1'
r = requests.get(url)
print r.status_code
#print r.text
print r.json()