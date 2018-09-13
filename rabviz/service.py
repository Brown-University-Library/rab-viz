import os
import json

from flask import Flask, jsonify, request
import pymongo

from config.settings import config

app = Flask(__name__)
mongo = pymongo.MongoClient(config['MONGO_URI'], config['MONGO_PORT'])
mongo_db = mongo.get_database(config['MONGO_DB'])
auth = mongo_db.authenticate(
    config['MONGO_USER'], config['MONGO_PASSWORD'])

@app.route('/')
def collection_index():
    # Returns a list of available data collections
    # Ex: coauthors, collaborators
    base_url = request.base_url
    graph_options = mongo_db.list_collection_names()
    reserved = [ 'system.indexes' ]
    return jsonify({ opt: '{0}{1}/'.format(base_url, opt)
                        for opt in graph_options if opt not in reserved })

@app.route('/<collection>/')
def collection_key_index(collection):
    # Returns a list of links to individual documents
    # in each collection, keyed on VIVO URI, with link
    # to document within collection using base_url
    base_url = request.base_url
    try:
        coll = mongo_db[collection]
    except:
        return {}
    all_docs = coll.find()
    data = { doc['rabid'] : base_url + doc['rabid'][33:] for doc in all_docs}
    return jsonify(data)

@app.route('/<collection>/<shortid>')
def get_document_data_by_shortid(collection, shortid):
    # Return a document from a collection
    # by shortID. Optional parameter "ds"
    # returns the document data in a particular
    # structure; ie matrix, graph
    data_structure = request.args.get('ds',None) 
    coll = mongo_db[collection]
    data = coll.find_one(
        {"rabid": "http://vivo.brown.edu/individual/{0}".format(shortid)})
    if data:
        data['updated'] = data['updated'].strftime('%Y-%m-%d')
        del data['_id']
        if data_structure:
            return jsonify({ 'data': data[data_structure],
                'updated': data['updated'] })
        else:
            return jsonify(data)
    else:
        return jsonify({})

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)
