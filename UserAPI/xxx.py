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