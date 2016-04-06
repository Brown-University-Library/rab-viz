"https://pymotw.com/2/sqlite3/"

import csv
import os
import sqlite3

db_filename = 'visualizations.db'

chord_dept_data_file = "../ingest/chords/data_out/chord_data.csv"
chord_dept_sql =	"""
					insert into chord_dept_viz
					(deptid, facultykey, facultydata)
					values (?, ?, ?)
					"""

faculty_data_file = "../ingest/faculty/data_in/faculty_in.csv"
faculty_sql =	"""
					insert into faculty
					(rabid,shortid,firstname,lastname,fullname,nameabbrev,preftitle,email,primarydept)
					values (?, ?, ?, ?, ?, ?, ?, ?, ?)
					"""

dept_data_file 	= "../ingest/depts/data_in/dept_in.csv"
dept_sql		=	"""
					insert into department
					(rabid,label)
					values (?, ?)
					"""

with sqlite3.connect(db_filename) as conn:
		print 'DELETING DATA'

		cursor = conn.cursor()
		delete_script = """
						DELETE FROM {0}
						"""
		tables = ["faculty", "chord_dept_viz", "department"]
		for t in tables:
			cursor.execute(delete_script.format(t))
		cursor.execute("VACUUM")

		print "Seeding database"

		with open(chord_dept_data_file, 'rt') as csv_file:
			csv_reader = csv.reader(csv_file)
			chord_dept_seeds = [ tuple([row[0],row[1],row[2]])
						for row in csv_reader]

		with open(faculty_data_file, 'rt') as csv_file:
			csv_reader = csv.reader(csv_file)
			faculty_seeds = [ tuple([row[0],row[1],row[2],
									row[3],row[4],row[5],
									row[6],row[7],row[8]])
						for row in csv_reader]

		with open(dept_data_file, 'rt') as csv_file:
			csv_reader = csv.reader(csv_file)
			dept_seeds = [ tuple([row[0],row[1]])
						for row in csv_reader]

		cursor.executemany(chord_dept_sql, chord_dept_seeds)
		cursor.executemany(faculty_sql, faculty_seeds)
		cursor.executemany(dept_sql, dept_seeds)