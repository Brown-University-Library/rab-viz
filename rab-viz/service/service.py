import os
import json

from flask import Flask, jsonify

from config.settings import config

app = Flask(__name__)
edgeDir = config['EDGE_DIR']

@app.route('/edgegraph/<shortid>')
def edgegraph(shortid):
	with open( os.path.join(edgeDir, shortid + '.json') ) as f:
		data = json.load(f)
	return jsonify(data)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)