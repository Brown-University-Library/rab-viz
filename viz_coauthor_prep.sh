#!/bin/bash
set -e

# #Necessary for Python
# LD_LIBRARY_PATH=/usr/local/lib
# export LD_LIBRARY_PATH


# HOME=/opt/local/vivo-maintenance-queries

# cd $HOME

# #set env
# source $HOME/venv/bin/activate
# #env vars
# source $HOME/venv/bin/vivoenv.sh

#Updates
python db/etl/extract/scripts/download_rab_data.py
python vmq/run.py --directory ./vmq/jobs/pub_ids/ --update
python vmq/run.py --directory ./vmq/jobs/research_areas/ --update
python vmq/run.py --directory ./vmq/jobs/search_index/ --update

#Merge
python vmq/run.py --directory ./vmq/jobs/merge --merge


#Exit Python venv
deactivate