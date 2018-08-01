import os
import csv
import sys
import logging
import pymongo

from config.settings import config
from etl.transform import coauthorGraph, coauthorMatrix
from etl.transform import collaboratorGraph, collaboratorOrgs

logging.basicConfig(
    filename=os.path.join(config['LOG_DIR'],'example.log'),
    format='%(asctime)-15s %(message)s',
    level=logging.DEBUG)

rab_jobs  = [ coauthorGraph, coauthorMatrix,
    collaboratorGraph, collaboratorOrgs ]

def load_csv(fileName):
    with open(fileName, 'r' ) as f:
        rdr = csv.reader(f)
        data = [ row for row in rdr ]
    return data

def main():
    extractDir = config['EXTRACT_DIR']
    mongo = pymongo.MongoClient(config['MONGO_URI'])
    viz_db = mongo.get_database(config['MONGO_DB'])

    for job in rab_jobs:
        viz_coll = viz_db[ job.collection_name ]
        coll_key = job.key_field
        coll_val = job.value_field

        datasets = []
        for input_file in job.input_files:
            data = load_csv(os.path.join(extractDir, input_file) )
            datasets.append(data)

        data_generator = job.transform(*datasets)
        for key, timestamp, trans_data in data_generator:
            viz_coll.update_one({ coll_key: key },
                {'$set' : { 'updated': timestamp, coll_key: key,
                coll_val: trans_data } }, upsert=True)


if __name__ == "__main__":
    main()
