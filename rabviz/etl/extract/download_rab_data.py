import os
import io
import csv
import sys
import requests
import logging

from config.settings import config
import validators
from jobs import faculty, departments, affiliations, coauthors

logging.basicConfig(
    filename=os.path.join(config['LOG_DIR'],'example.log'),
    format='%(asctime)-15s %(message)s',
    level=logging.DEBUG)

adminEmail = config['ADMIN_EMAIL']
adminPass = config['ADMIN_PASSWORD']
queryAPI = config['RAB_QUERY_API']
destinationDir = os.path.join(config['DATA_DIR'], 'raw')

rab_jobs  = [ faculty, departments, affiliations, coauthors ]

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
        resp = query_vivo_api(job.query)
        data = process_response(resp)
        validated = job.validate(data)
        if ( len(validated) == 1 and 
                isinstance(validated[0], validators.Invalid) ) :
            logging.error("Invalid dataset: " + job.__name__)
            continue
        invalid = [ (e, row._msg) for e, row in enumerate(validated)
                    if isinstance(row, validators.Invalid) ]
        valid = [ row for row in validated
                    if not isinstance(row, validators.Invalid) ]
        if invalid != []:
            for i in invalid:
                logging.debug(
                    "Invalid data::{0} line {1}: {2}".format(
                        job.__name__, i[0], i[1] ) )
        destination = os.path.join(destinationDir, job.destination)
        with open(destination,'w') as dataout:
          wrtr = csv.writer(dataout)
          wrtr.writerows(valid)

if __name__ == "__main__":
    main()
