from collections import defaultdict
import sys
import csv
import os
import json

def main(inFileFac, inFileDept, inFileAffs, targetDir):
	if not os.path.exists(targetDir):
		os.makedirs(targetDir)

	depts = dict()
	affs = dict()
	facs = []
	facList = []
	deptFacList = defaultdict(set)

	with open(inFileDept, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		#Skip header
		head = rdr.next()
		# deptid, label
		for row in rdr:
			depts[row[0]] = row[1]

	with open(inFileFac, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		#Skip header
		head = rdr.next()
		# rabid, last, first, label, title 
		for row in rdr:
			facs.append((row[0], row[1], row[2], row[3], row[4]))
			facList.append(row[0])

	with open(inFileAffs, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		#Skip header
		head = rdr.next()
		# facid, deptid, rank(?)
		for row in rdr:
			if depts.get(row[1]) and row[0] in facList:
				deptFacList[row[1]].add(row[0])
			# Only interested in positions ranked 1
			# This also skips unranked positions (val=0)
			if row[2] != 1:
				continue
			if not affs.get(row[0]):
				# no affiliations associated with the rabid
				# in affs dict, so...
				if depts.get(row[1]):
					# lookup deptid from affiliation in dept dict...
					affs[row[0]] = depts[row[1]]
				else:
					# if there is no corresponding entry (ie, a
					# dept that no longer exists), list "Other"
					affs[row[0]] = "Other"
			else:
				# If there is already a value in the affs dict,
				# that means there are multiple affs for this rabid
				affs[row[0]] = "Multiple"

	with open(
			os.path.join(targetDir,'faculty_data.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		for fac in facs:
			rabid, last, first, name, title = fac
			abbrev = last + ", " + first[0]
			if affs.get(rabid):
				deptLabel = affs[rabid]
			else:
				deptLabel = "None"
			row = (rabid, last, first, name, abbrev, title, deptLabel)
			wrtr.writerow(row)

	with open(
			os.path.join(targetDir,'affiliations_json.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		for d in deptFacList:
			row = (d, json.dumps(list(deptFacList[d])))
			wrtr.writerow(row)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])