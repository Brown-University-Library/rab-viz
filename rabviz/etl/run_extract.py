import os
import io
import csv
import sys
import requests
import logging

from config.settings import config
from etl.extract import faculty, departments, affiliations
from etl.extract import coauthors, collaborators

logging.basicConfig(
    filename=os.path.join(config['LOG_DIR'],'etl.log'),
    format='%(asctime)-15s %(message)s',
    level=logging.INFO)

adminEmail = config['ADMIN_EMAIL']
adminPass = config['ADMIN_PASSWORD']
queryAPI = config['RAB_QUERY_API']
destinationDir = config['EXTRACT_DIR']

rab_jobs  = [ faculty, departments, affiliations,
    coauthors, collaborators ]

def process_response(rawText):
    rdr = csv.reader( io.StringIO(rawText) )
    return [ row for row in rdr ]


def query_vivo_api(query):
    post_data = {   'query' : query,
                    'password': adminPass,
                    'email': adminEmail }
    header = { 'Accept': 'text/csv' }
    resp = requests.post(queryAPI, data=post_data, headers=header)
    if resp.status_code == 200:
        return resp.text
    else:
        return ''

def main():
    for job in rab_jobs:
        logging.info("Begin: " + job.__name__)
        resp = query_vivo_api(job.query)
        data = process_response(resp)
        validated = job.validate(data)
        if ( len(validated) == 1 and getattr(validated[0], "invalid", False) ) :
            logging.error("Invalid dataset: " + job.__name__)
            continue
        invalid = [ (e, row._msg) for e, row in enumerate(validated)
                    if getattr(row, "invalid", False) ]
        valid = [ row for row in validated
                    if not getattr(row, "invalid", False) ]
        if invalid != []:
            for i in invalid:
                logging.debug(
                    "Invalid data::{0} line {1}: {2}".format(
                        job.__name__, i[0], i[1] ) )
        destination = os.path.join(destinationDir, job.destination)
        with open(destination,'w') as dataout:
          wrtr = csv.writer(dataout)
          wrtr.writerows(valid)
        logging.info("Completed: " + job.__name__)

if __name__ == "__main__":
    main()
