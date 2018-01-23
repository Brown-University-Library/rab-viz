import os
import csv
import sys
import requests

from config.settings import config
from jobs import faculty, departments

adminEmail = config['ADMIN_EMAIL']
adminPass = config['ADMIN_PASSWORD']
queryAPI = config['RAB_QUERY_API']
destinationDir = os.path.join(config['DATA_DIR'], 'raw')

rab_jobs  = [ faculty, departments ]

def process_response(rawText):
    rdr = csv.reader(rawText)
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
        destination = os.path.join(destinationDir, job.destination)
        with open(destination,'w') as dataout:
          wrtr = csv.writer(dataout, delimiter=",")
          wrtr.writerows(data)

if __name__ == "__main__":
    main()
