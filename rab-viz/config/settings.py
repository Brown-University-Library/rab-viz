import os

settings = {
	'APP_ROOT' : os.path.abspath(__file__ + "/../../"),
	'RAB_QUERY_API': '',
	'ADMIN_EMAIL' : '',
	'ADMIN_PASSWORD' : '',
}

settings['DATA_DIR'] = os.path.join(settings['APP_ROOT'], 'data')