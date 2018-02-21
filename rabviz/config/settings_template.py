import os

config = {
    'APP_ROOT' : os.path.abspath(__file__ + "/../../"),
    'RAB_QUERY_API': '',
    'ADMIN_EMAIL' : '',
    'ADMIN_PASSWORD' : '',
    'MONGO_URI' : '',
    'MONGO_DB' : ''
}

config['DATA_DIR'] = os.path.join(config['APP_ROOT'], 'data')
config['EXTRACT_DIR'] = os.path.join(config['DATA_DIR'], 'extract')
config['LOG_DIR'] = os.path.join(config['APP_ROOT'], 'logs')