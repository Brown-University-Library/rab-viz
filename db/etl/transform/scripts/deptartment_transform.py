import sys
import csv
import os
import json
from collections import defaultdict

def main(inDeptFile, inAffsFile, targetDir):
	if not os.path.exists(targetDir):
		os.makedirs(targetDir)

	depts = dict()
	rosters = defaultdict(set)

	with open(inDeptFile, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		#Skip header
		head = rdr.next()
		#Auth1URI, Auth2URI, CitationURI
		for row in rdr:
			# Handle departments with more than 1 label
			if depts.get(row[0]):
				continue
			else:
				depts[row[0]] = row[1]

	with open(
			os.path.join(targetDir,'departments_data.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		for deptid, label in depts.items():
			row = (deptid, label)
			wrtr.writerow(row)

	with open(inAffsFile, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		#Skip header
		head = rdr.next()
		#Auth1URI, Auth2URI, CitationURI
		for row in rdr:
			# Handle departments with more than 1 label
			if depts.get(row[1]):
				rosters[row[1]].add(row[0])
			else:
				continue

	with open(
			os.path.join(targetDir,'dept_roster_data.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		for dept, rset in rosters.items():
			row = (dept, json.dumps(list(rset)))
			wrtr.writerow(row)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3])