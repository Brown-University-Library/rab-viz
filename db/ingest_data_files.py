"https://pymotw.com/2/sqlite3/"

import csv
import os
import sqlite3

db_filename = 'visualizations.db'

faculty_data_file = "../ingest/transform/transformed/faculty_data.csv"
faculty_sql =	"""
					insert into faculty
					(rabid,lastname,firstname,fullname,abbrev,title,deptLabel)
					values (?, ?, ?, ?, ?, ?, ?)
					"""

dept_data_file 	= "../ingest/transform/transformed/departments_data.csv"
dept_sql		=	"""
					insert into departments
					(rabid,label)
					values (?, ?)
					"""

coauthors_data_file = "../ingest/transform/transformed/coauthors_data.csv"
coauthors_sql =		"""
					insert into coauthors
					(authid, coauthid, cnt)
					values (?, ?, ?)
					"""

author_json_data_file = "../ingest/transform/transformed/author_json_data.csv"
author_json_sql =	"""
					insert into author_json
					(facid, jsondata)
					values (?, ?)
					"""

affiliations_data_file = "../ingest/transform/transformed/affiliations_data.csv"
affiliations_sql =	"""
					insert into affiliations
					(facid, deptid, rank)
					values (?, ?, ?)
					"""

with sqlite3.connect(db_filename) as conn:
		print 'DELETING DATA'

		cursor = conn.cursor()
		delete_script = """
						DELETE FROM {0}
						"""
		tables = [	"faculty",
					"departments",
					"coauthors",
					"author_json",
					"affiliations"]
		for t in tables:
			cursor.execute(delete_script.format(t))
		cursor.execute("VACUUM")

		print "Seeding database"

		with open(faculty_data_file, 'rt') as csv_file:
			csv_reader = csv.reader(csv_file)
			faculty_seeds = [ tuple([row[0],row[1],row[2],
									row[3],row[4],row[5],
									row[6]])
						for row in csv_reader]

		with open(dept_data_file, 'rt') as csv_file:
			csv_reader = csv.reader(csv_file)
			dept_seeds = [ tuple([row[0],row[1]])
						for row in csv_reader]

		with open(coauthors_data_file, 'rt') as csv_file:
			csv_reader = csv.reader(csv_file)
			coauthors_seeds = [ tuple([row[0],row[1],row[2]])
						for row in csv_reader]

		with open(author_json_data_file, 'rt') as csv_file:
			csv_reader = csv.reader(csv_file)
			author_json_seeds = [ tuple([row[0],row[1]])
						for row in csv_reader]

		with open(affiliations_data_file, 'rt') as csv_file:
			csv_reader = csv.reader(csv_file)
			affiliations_seeds = [ tuple([row[0],row[1], row[2]])
						for row in csv_reader]

		cursor.executemany(faculty_sql, faculty_seeds)
		cursor.executemany(dept_sql, dept_seeds)
		cursor.executemany(coauthors_sql, coauthors_seeds)
		cursor.executemany(author_json_sql, author_json_seeds)
		cursor.executemany(affiliations_sql, affiliations_seeds)