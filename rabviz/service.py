import os
import json

from flask import Flask, jsonify, request
import pymongo

from config.settings import config

app = Flask(__name__)
mongo = pymongo.MongoClient(config['MONGO_URI'])
mongo_db = mongo.get_database(config['MONGO_DB'])

@app.route('/')
def graph_index():
    base_url = request.base_url
    graph_options = mongo_db.collection_names()
    reserved = [ 'system.indexes' ]
    return jsonify({ opt: '{0}{1}/'.format(base_url, opt)
                        for opt in graph_options if opt not in reserved })

@app.route('/<viz>/')
def graph_subject_index(viz):
    base_url = request.base_url
    try:
        coll = mongo_db[viz]
    except:
        return {}
    all_docs = coll.find()
    data = { doc['rabid'] : base_url + doc['rabid'][33:] for doc in all_docs}
    return jsonify(data)

@app.route('/<viz>/<shortid>')
def get_viz_data_by_shortid(viz, shortid):
    coll = mongo_db[viz]
    data = coll.find_one({"rabid": "http://vivo.brown.edu/individual/{0}".format(shortid)})
    if data:
        return jsonify({
            'data': data['data'],
            'updated': data['updated'].strftime('%Y-%m-%d') })
    else:
        return jsonify({})

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)
