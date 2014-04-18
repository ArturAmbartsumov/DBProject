from django.views.decorators.csrf import csrf_exempt

from Forum.dbService import functions as Util

@csrf_exempt
def clear(request):
	get_cursor = Util.sendQuery("SET foreign_key_checks = 0", [])
	if get_cursor['err'] != 0: return Util.HttpResponseJSONFailure(get_cursor['err'])
	get_cursor = Util.sendQuery("TRUNCATE TABLE Subscriptions", [])
	if get_cursor['err'] != 0: return Util.HttpResponseJSONFailure(get_cursor['err'])
	get_cursor = Util.sendQuery("TRUNCATE TABLE Followers", [])
	if get_cursor['err'] != 0: return Util.HttpResponseJSONFailure(get_cursor['err'])
	get_cursor = Util.sendQuery("TRUNCATE TABLE Posts", [])
	if get_cursor['err'] != 0: return Util.HttpResponseJSONFailure(get_cursor['err'])
	get_cursor = Util.sendQuery("TRUNCATE TABLE Threads", [])
	if get_cursor['err'] != 0: return Util.HttpResponseJSONFailure(get_cursor['err'])
	get_cursor = Util.sendQuery("TRUNCATE TABLE Forums", [])
	if get_cursor['err'] != 0: return Util.HttpResponseJSONFailure(get_cursor['err'])
	get_cursor = Util.sendQuery("TRUNCATE TABLE Users", [])
	if get_cursor['err'] != 0: return Util.HttpResponseJSONFailure(get_cursor['err'])
	get_cursor = Util.sendQuery("SET foreign_key_checks = 1", [])
	if get_cursor['err'] != 0: return Util.HttpResponseJSONFailure(get_cursor['err'])

	return Util.HttpResponseJSONSuccess("Database successfully cleared!")
