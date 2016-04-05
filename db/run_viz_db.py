"https://pymotw.com/2/sqlite3/"

import csv
import os
import sqlite3

db_filename = 'visualizations.db'
schema_filename = 'schema.sql'

db_is_new = not os.path.exists(db_filename)

chord_dept_data_file = "../chords/ingest/data_out/chord_data.csv"
chord_dept_sql =	"""
					insert into chord_dept_viz
					(deptid, facultykey, facultydata)
					values (?, ?, ?)
					"""

with sqlite3.connect(db_filename) as conn:
	if db_is_new:
		print 'Creating schema'
		with open(schema_filename, 'rt') as f:
			schema = f.read()
		conn.executescript(schema)

		print "Seeding database"

		with open(chord_dept_data_file, 'rt') as csv_file:
			csv_reader = csv.reader(csv_file)
			seeds = [ tuple([row[0],row[1],row[2]])
						for row in csv_reader]
		cursor = conn.cursor()
		cursor.executemany(chord_dept_sql, seeds)

	else:
		print "Database exists"