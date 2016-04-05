"https://pymotw.com/2/sqlite3/"

import csv
import os
import sqlite3

db_filename = 'visualizations.db'
schema_filename = 'schema.sql'
viz_data = 'viz-seeds.csv'
fac_data = 'fac-seeds.csv'

db_is_new = not os.path.exists(db_filename)
bulk_sql =	"""
			insert into triples (subject, predicate, object)
			values (?, ?, ?)
			"""

with sqlite3.connect(db_filename) as conn:
	if db_is_new:
		print 'Creating schema'
		with open(schema_filename, 'rt') as f:
			schema = f.read()
		conn.executescript(schema)

		print "Seeding database"

		with open(test_data, 'rt') as csv_file:
			csv_reader = csv.reader(csv_file)
			seeds = [ tuple([
						unicode(row[0], errors='replace'),
						unicode(row[1], errors='replace'),
						unicode(row[2], errors='replace')
						]) for row in csv_reader]
		cursor = conn.cursor()
		cursor.executemany(bulk_sql, seeds)

	else:
		print "Database exists"