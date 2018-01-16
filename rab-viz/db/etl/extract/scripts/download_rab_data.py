import os
import csv
import sys
import requests

from config.development import settings as config
# from rdflib import ConjunctiveGraph
# from rdflib.query import ResultException
# from vdm.namespaces import ns_mgr

# endpoint = os.getenv('VIVO_ENDPOINT')
# if endpoint is None:
#     raise Exception("No VIVO endpoint found.  Set environment variable.")
# vstore = ConjunctiveGraph('SPARQLStore')
# vstore.open(endpoint)
# vstore.namespace_manager = ns_mgr

adminEmail = config['ADMIN_EMAIL']
adminPass = config['ADMIN_PASSWORD']
queryAPI = config['RAB_QUERY_API']
queryTemplate = "{0} SELECT {1} WHERE {{{2}}}"

jobs = [
  {
    "name": "faculty",
    "ns" : """PREFIX rdfs:     <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX blocal:   <http://vivo.brown.edu/ontology/vivo-brown/>
    PREFIX foaf:     <http://xmlns.com/foaf/0.1/>
    PREFIX vivo:     <http://vivoweb.org/ontology/core#>
    """,
    "select": "?id ?last ?first ?label ?title ?org",
    "where": """
      ?id a vivo:FacultyMember .
      ?id a blocal:BrownThing .
      ?id foaf:lastName ?last .
      ?id foaf:firstName ?first .
      ?id rdfs:label ?label .
      ?id vivo:preferredTitle ?title .
      OPTIONAL {?id blocal:primaryOrgLabel ?org .}
    """,
    "target": "faculty.csv"
  },
  {
    "name": "coauthors",
    "ns" : """PREFIX bcite:    <http://vivo.brown.edu/ontology/citation#>
    PREFIX blocal:   <http://vivo.brown.edu/ontology/vivo-brown/>
    PREFIX vivo:     <http://vivoweb.org/ontology/core#>
    """,
    "select": "?fac1 ?fac2 ?cite",
    "where": """
      ?cite a bcite:Citation .
      ?cite bcite:hasContributor ?fac1 .
      ?cite bcite:hasContributor ?fac2 .
      ?fac1 a vivo:FacultyMember .
      ?fac1 a blocal:BrownThing .
      FILTER (?fac1 != ?fac2)
    """,
    "target": "coauthors.csv"
  },
  {
    "name": "departments",
    "ns" : """PREFIX rdfs:     <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX blocal:   <http://vivo.brown.edu/ontology/vivo-brown/>
    PREFIX foaf:     <http://xmlns.com/foaf/0.1/>
    """,
    "select": "DISTINCT ?dept ?name",
    "where": """
      ?dept a foaf:Organization .
      ?dept a blocal:BrownThing .
      ?dept rdfs:label ?label .
      BIND(str(?label) as ?name) .
    """,
    "target": "departments.csv"
  },
  {
    "name": "affiliations",
    "ns" : """PREFIX blocal:   <http://vivo.brown.edu/ontology/vivo-brown/>
    PREFIX vivo:     <http://vivoweb.org/ontology/core#>
    """,
    "select": "?id ?dept ?rank",
    "where": """
      ?id a vivo:FacultyMember .
      ?id a blocal:BrownThing .
      ?id vivo:personInPosition ?pos .
      ?pos vivo:positionInOrganization ?dept .
      OPTIONAL {?pos vivo:rank ?rank .}
    """,
    "target": "affiliations.csv"
  },
]


def query_vivo_api(rq):
    post_data = {   'query' : rq,
                    'password': adminPass,
                    'email': adminEmail }
    header = { 'Accept': 'text/csv' }
    resp = requests.post(queryAPI, data=post_data, headers=header)
    if resp.status_code == 200:
        return resp.text
    else:
        return ''

def main(targetDir):
  for job in jobs:
    query = queryTemplate.format(job['ns'], job['select'], job['where'])
    resp = query_vivo_api(query)
    with open(
      os.path.join(targetDir, job['target']),'w') as dataout:
      wrtr = csv.writer(dataout)
      wrtr.writerows(resp)

if __name__ == "__main__":
  main(sys.argv[1])