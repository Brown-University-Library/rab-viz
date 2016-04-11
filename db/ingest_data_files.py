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

chord_fac_data_file = "../ingest/faculty/data_out/fac_chord_data.csv"
chord_fac_sql =	"""
					insert into chord_fac_viz
					(facid, coauthkey, coauthdata)
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

force_fac_data_file = "../ingest/faculty/data_out/fac_force_data.csv"
force_fac_sql =		"""
					insert into force_fac_viz
					(facid, nodeuris, links)
					values (?, ?, ?)
					"""

force_dept_data_file = "../ingest/chords/data_out/dept_force_data.csv"
force_dept_sql =		"""
					insert into force_dept_viz
					(deptid, nodeuris, links)
					values (?, ?, ?)
					"""

with sqlite3.connect(db_filename) as conn:
		print 'DELETING DATA'

		cursor = conn.cursor()
		delete_script = """
						DELETE FROM {0}
						"""
		tables = ["faculty", "chord_dept_viz", "department", "chord_fac_viz", "force_fac_viz", "force_dept_viz"]
		for t in tables:
			cursor.execute(delete_script.format(t))
		cursor.execute("VACUUM")

		print "Seeding database"

		with open(chord_dept_data_file, 'rt') as csv_file:
			csv_reader = csv.reader(csv_file)
			chord_dept_seeds = [ tuple([row[0],row[1],row[2]])
						for row in csv_reader]

		with open(chord_fac_data_file, 'rt') as csv_file:
			csv_reader = csv.reader(csv_file)
			chord_fac_seeds = [ tuple([row[0],row[1],row[2]])
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

		with open(force_fac_data_file, 'rt') as csv_file:
			csv_reader = csv.reader(csv_file)
			force_fac_seeds = [ tuple([row[0],row[1],row[2]])
						for row in csv_reader]

		with open(force_dept_data_file, 'rt') as csv_file:
			csv_reader = csv.reader(csv_file)
			force_dept_seeds = [ tuple([row[0],row[1],row[2]])
						for row in csv_reader]

		cursor.executemany(chord_dept_sql, chord_dept_seeds)
		cursor.executemany(chord_fac_sql, chord_fac_seeds)
		cursor.executemany(faculty_sql, faculty_seeds)
		cursor.executemany(dept_sql, dept_seeds)
		cursor.executemany(force_fac_sql, force_fac_seeds)
		cursor.executemany(force_dept_sql, force_dept_seeds)