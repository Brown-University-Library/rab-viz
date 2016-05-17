import os
import csv

from rdflib import ConjunctiveGraph
from rdflib.query import ResultException
from vdm.namespaces import ns_mgr

endpoint = os.getenv('VIVO_ENDPOINT')
if endpoint is None:
    raise Exception("No VIVO endpoint found.  Set environment variable.")
vstore = ConjunctiveGraph('SPARQLStore')
vstore.open(endpoint)
vstore.namespace_manager = ns_mgr


targetDir = "/work/viz/db/etl/extract/data"
queryTemplate = "SELECT {0} WHERE {{{1}}}"
jobs = [
  {
    "name": "faculty",
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


def queryRAB(rq):
    try:
        rsp = vstore.query(rq)
        return rsp
    except ResultException:
        logging.info("No results found for query: {0}".format(rq))
        return Graph()

def main():
  for job in jobs:
    query = queryTemplate.format(job['select'], job['where'])
    resp = queryRAB(query)
    with open(
      os.path.join(targetDir, job['target']),'w') as dataout:
      wrtr = csv.writer(dataout)
      wrtr.writerows(resp)

if __name__ == "__main__":
  main()