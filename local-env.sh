#!/bin/bash

export VIVO_URL='http://localhost:8080/rab/'
export VIVO_SOLR_URL='http://localhost:8080/rabsolr/'
export VIVO_USER='vivo_root@brown.edu'
export VIVO_PASS='goVivo'
export VIVO_NAMESPACE='http://vivo.brown.edu/individual/'
#Expecting Fuseki.
export VIVO_ENDPOINT='http://localhost:8082/VIVO/query'
export VIVO_MANAGER_AUTH='None'
export DATA_NAMESPACE='http://vivo.brown.edu/individual/'
export VDM_USER_AGENT='Brown University Library http://vivo.brown.edu'
export CROSSREF_EMAIL='tlawless@brown.edu'

PWD=`pwd`
PYTHONPATH="${PYTHONPATH}:/$PWD"
export PYTHONPATH