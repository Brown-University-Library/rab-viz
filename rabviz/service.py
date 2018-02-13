import os
import json

from flask import Flask, jsonify
import pymongo

from config.settings import config

app = Flask(__name__)
mongo = pymongo.MongoClient('localhost', 27017)
mongo_db = mongo.get_database('rabviz')

@app.route('/')
def base_index():
	return "Viz index !"

@app.route('/edgegraph/')
def edge_index():
	return "Edgegraph !"

@app.route('/edgegraph/<shortid>')
def edgegraph(shortid):
    coll = mongo_db['forceEdge']
    data = coll.find_one({"rabid": "http://vivo.brown.edu/individual/{0}".format(shortid)})
    if data:
        return jsonify(data['data'])
    else:
        return jsonify({})

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)
