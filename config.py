import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/visualizations.db')
VIVO_DATA_SERVICE='https://vivo.brown.edu/services/data/v1/'
VIVO_GRAPH_SERVICE='http://localhost:8000/'