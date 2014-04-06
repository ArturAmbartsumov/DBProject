
##########################################
# Всякий хлам, не используемый в проекте #
##########################################

def create(request):
	if request.method != 'POST': return HttpResponseJSONFailure("Method POST is expected")
	print 5555555
	request_data = json.loads(request.body)
	print request_data
	try: 
		username = request_data['username']
		about = request_data['about']
		name = request_data['name']
		email = request_data['email']
	except KeyError as e:
		return HttpResponseJSONFailure(str(e))
	isAnonymous = request_data.get('isAnonymous', False)

	cursor = connection.cursor()
	try:
		with transaction.atomic():
			cursor.execute("INSERT INTO users (username, email, name, about, isAnonymous)" + "VALUES (%s, %s, %s, %s, %s)", [username, email, name, about, isAnonymous])
	except IntegrityError as e:
		return HttpResponseJSONFailure(str(e))

	cursor.execute("SELECT * FROM users WHERE email=%s", [email])
	return HttpResponseJSONSuccess(dictfetchall(cursor))
	return HttpResponseJSONSuccess(json.dumps(request_data))

{u'code': 0, 
u'response': 

  [{u'username': u'user2', 
	u'about': u'hello im user2', 
	u'name': u'John', 
	u'subscriptions': [1], 
	u'id': 2, 
	u'followers': [u'user3@mail.ru', u'user4@mail.ru'], 
	u'following': [u'user1@mail.ru', u'user5@mail.ru'], 
	u'isAnonymous': 0, 
	u'email': u'user2@mail.ru'}, 

   {u'username': u'user4', 
    u'about': u'hello im user4', 
    u'name': u'John', 
    u'subscriptions': [1], 
    u'id': 4, 
    u'followers': [], 
    u'following': [u'user1@mail.ru', u'user2@mail.ru'], 
    u'isAnonymous': 0, 
    u'email': u'user4@mail.ru'}, 

   {u'username': u'user3', 
    u'about': u'hello im user3', 
    u'name': u'John', 
    u'subscriptions': [1], u'id': 3, 
    u'followers': [u'user1@mail.ru'], 
    u'following': [u'user1@mail.ru', u'user2@mail.ru'], 
    u'isAnonymous': 0, u'email': 
    u'user3@mail.ru'}
  ]
}






















