import json
import requests
import datetime

url = 'http://127.0.0.1:8000/user/create/'
payload = {'username': 'sdfg', 'about': 'hdf', 'isAnonymous': False, 'name': 'sdf', 'email': 'Artur@mail.ru'}
r = requests.post(url, data=json.dumps(payload))
print r.status_code
#print r.text
print r.json()

url = 'http://127.0.0.1:8000/forum/create/'
payload = {'name': 'Forum 6', 'short_name': 'forum_6', 'user': 'user2@mail.ru'}
r = requests.post(url, data=json.dumps(payload))
print r.status_code
#print r.text
print r.json()

url = 'http://127.0.0.1:8000/thread/create/'
payload = {'forum': 'forum_3',
		   'title': 'Tred 7',
		   'isClosed': False,
		   'user': 'user4@mail.ru',
		   'date': (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
		   'message': 'messageTred7',
		   'slug': 'tred_7',
		   'isDeleted': False}
r = requests.post(url, data=json.dumps(payload))
print r.status_code
#print r.text
print r.json()

url = 'http://127.0.0.1:8000/post/create/'
payload = {'isApproved': True,
		   'user': 'user5@mail.ru',
		   'date': (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
		   'message': 'message post 1',
		   'isSpam': False,
		   'isHighlighted': True,
		   'thread': 23,
		   'forum': 'forum_5',
		   'isDeleted': False,
		   'isEdited': True,
		   'parent': 7}
r = requests.post(url, data=json.dumps(payload))
print r.status_code
#print r.text
print r.json()

payload = {'user': 'user5@mail.ru'}
url = 'http://127.0.0.1:8000/user/details/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()

payload = {'related': ['user'], 'forum': 'forum_3'}
url = 'http://127.0.0.1:8000/forum/details/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()

payload = {'related': ['user', 'forum'], 'thread': '2'}
url = 'http://127.0.0.1:8000/thread/details/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()

payload = {'related': ['user', 'forum', 'thread'], 'post': '6'}
url = 'http://127.0.0.1:8000/post/details/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()

url = 'http://127.0.0.1:8000/user/unfollow/'
payload = {'follower': 'user5@mail.ru'}
r = requests.post(url, data=json.dumps(payload))
print r.status_code
#print r.text
print r.json()

import json
import requests
payload = {'user': 'user3@mail.ru', 'order': 'asc'}
url = 'http://127.0.0.1:8000/user/listFollowers/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()

import json
import requests
payload = {'user': 'user5@mail.ru'}
url = 'http://127.0.0.1:8000/user/listFollowing/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()

import json
import requests
payload = {'user': 'user5@mail.ru', 'order': 'asc', 'since': '2014-04-14 21:27:34'}
url = 'http://127.0.0.1:8000/user/listPosts/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()

import json
import requests
url = 'http://127.0.0.1:8000/user/updateProfile/'
payload = {'about': 'Hello im Artur', 'user': 'Artur@mail.ru', 'name': 'Artur'}
r = requests.post(url, data=json.dumps(payload))
print r.status_code
#print r.text
print r.json()

payload = {'related': ['thread'],
		   'since': '2014-01-02 00:00:00',
		   'limit': 2, 'order': 'asc',
		   'forum': 'forum_5'}
url = 'http://127.0.0.1:8000/forum/listPosts/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()

payload = {'user': 'user5@mail.ru', 'order': 'asc', 'since': '2014-04-14 21:27:34'}
url = 'http://127.0.0.1:8000/user/listPosts/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()

payload = {'thread': '2', 'order': 'asc', 'since': '2014-04-14 21:27:34'}
url = 'http://127.0.0.1:8000/thread/listPosts/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()

payload = {'limit': 10, 'since_id': 0, 'forum': 'forum_5', 'order': 'asc'}
url = 'http://127.0.0.1:8000/forum/listUsers/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()

payload = {'related': ['forum', 'user'],
		   'since': '2013-12-30 00:00:00',
		   'limit': 1,
		   'forum': 'forum_3',
		   'order': 'asc'}
url = 'http://127.0.0.1:8000/forum/listThreads/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()

payload = {'since': '2014-01-01 00:00:00', 'user': 'user1@mail.ru', 'order': 'desc'}
url = 'http://127.0.0.1:8000/thread/list/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()

payload = {'since': '2014-01-01 00:00:00', 'thread': '1', 'order': 'desc'}
url = 'http://127.0.0.1:8000/post/list/'
r = requests.get(url, params = payload)
print r.status_code
#print r.text
print r.json()
















