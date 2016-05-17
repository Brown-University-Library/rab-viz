"https://pymotw.com/2/sqlite3/"

import sys
import csv
import os
import sqlite3


def main(dbDir):
	db_filename = os.path.join(dbDir,'visualizations.db')
	schema_filename = os.path.join(dbDir,'schema.sql')

	db_is_new = not os.path.exists(db_filename)
	
	with sqlite3.connect(db_filename) as conn:
		if db_is_new:
			print 'Creating schema'
			with open(schema_filename, 'rt') as f:
				schema = f.read()
			conn.executescript(schema)
		else:
			print "Database exists"

if __name__ == "__main__":
	main(sys.argv[1])