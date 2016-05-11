"https://pymotw.com/2/sqlite3/"

import csv
import os
import sqlite3

db_filename = 'visualizations.db'
load_dir = "/work/viz/db/etl/load"

tables = {
	"faculty": {
		"file": os.path.join(load_dir,"faculty_data.csv"),
		"table": "faculty",
		"columns": ["rabid","lastname","firstname","fullname",
					"abbrev","title","deptLabel"]
	},
	"departments": {
		"file": os.path.join(load_dir,"departments_data.csv"),
		"table": "departments",
		"columns": ["rabid","label","useFor"]
	},
	"coauthors": {
		"file": os.path.join(load_dir,"coauthors_data.csv"),
		"table": "coauthors",
		"columns": ["authid","coauthid","cnt"]
	},
	"authorJson": {
		"file": os.path.join(load_dir,"author_json_data.csv"),
		"table": "author_json",
		"columns": ["facid", "jsondata"]
	},
	"affiliations": {
		"file": os.path.join(load_dir,"affiliations_data.csv"),
		"table": "affiliations",
		"columns": ["facid", "deptid", "rank"]
	},
	"chordDeptViz": {
		"file": os.path.join(load_dir,"chordDeptViz_data.csv"),
		"table": "chord_viz",
		"columns": ["rabid", "legend", "matrix"]
	},
	"chordFacViz": {
		"file": os.path.join(load_dir,"chordFacViz_data.csv"),
		"table": "chord_viz",
		"columns": ["rabid", "legend", "matrix"]
	}
} 

def writeSql(tableName, columnList):
	sql_template = """
				insert into {0}
				({1})
				values ({2})
				"""
	cStr = ",".join(columnList)
	qStr = ",".join(["?" for c in columnList])
	return sql_template.format(tableName, cStr, qStr)

def updateTable(cursor, tDict):
	with open(tDict["file"], 'rt') as csv_file:
		csv_reader = csv.reader(csv_file)
		seeds = [ tuple(row) for row in csv_reader ]
	sql = writeSql(tDict['table'],tDict['columns'])
	cursor.executemany(sql, seeds)

with sqlite3.connect(db_filename) as conn:
		print 'DELETING DATA'

		cursor = conn.cursor()
		delete_script = """
						DELETE FROM {0}
						"""
		for tDict in tables.values():
			cursor.execute(delete_script.format(tDict['table']))
		cursor.execute("VACUUM")

		print "Seeding database"

		for tDict in tables.values():
			updateTable(cursor, tDict)