#!/bin/bash
set -e

DB=/work/viz/db
ETL=/work/viz/db/etl
EXTRACT=/work/viz/db/etl/extract 
TRANSFORM=/work/viz/db/etl/transform
LOAD=/work/viz/db/etl/load

HOME=/work/viz/

cd $HOME
source $HOME/local-env.sh

#Clean out old data
rm $DB/visualizations.db
rm $EXTRACT/data/*
rm $TRANSFORM/data/*
rm $LOAD/*

#Download data from RAB
python $EXTRACT/scripts/download_rab_data.py

#Identity Tables
python $TRANSFORM/scripts/faculty_transform.py $EXTRACT/data/faculty.csv $EXTRACT/data/departments.csv $LOAD
python $TRANSFORM/scripts/affiliation_transform.py $EXTRACT/data/affiliations.csv $LOAD
python $TRANSFORM/scripts/coauth_transform.py $EXTRACT/data/coauthors.csv $EXTRACT/data/faculty.csv $LOAD
python $TRANSFORM/scripts/department_transform.py $EXTRACT/data/departments.csv $EXTRACT/data/faculty.csv $LOAD

#Roster data for department visualizations
python $TRANSFORM/scripts/roster_transform.py $EXTRACT/data/departments.csv $EXTRACT/data/affiliations.csv $TRANSFORM/data

#Visualization tables
python $TRANSFORM/scripts/viz_chord_fac.py $LOAD/author_json_data.csv $LOAD
python $TRANSFORM/scripts/viz_chord_dept.py $LOAD/author_json_data.csv $TRANSFORM/data/roster_data.csv $LOAD

python $TRANSFORM/scripts/viz_force_fac.py $LOAD/author_json_data.csv $LOAD
python $TRANSFORM/scripts/viz_force_dept.py $LOAD/author_json_data.csv $TRANSFORM/data/roster_data.csv $LOAD

# SQLite setup
python $DB/run_viz_db.py $DB
python $DB/ingest_data_files.py $DB $LOAD