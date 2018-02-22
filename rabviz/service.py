import os
import json

from flask import Flask, jsonify
import pymongo

from config.settings import config

app = Flask(__name__)
mongo = pymongo.MongoClient(config['MONGO_URI'])
mongo_db = mongo.get_database(config['MONGO_DB'])

@app.route('/')
def base_index():
	return "Viz index !"

@app.route('/edgegraph/')
def edge_index():
	return "Edgegraph !"

@app.route('/<viz>/<shortid>')
def get_viz_data_by_shortid(viz, shortid):
    coll = mongo_db[viz]
    data = coll.find_one({"rabid": "http://vivo.brown.edu/individual/{0}".format(shortid)})
    if data:
        return jsonify(data['data'])
    else:
        return jsonify({})

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)