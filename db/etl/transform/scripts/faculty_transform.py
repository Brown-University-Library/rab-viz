import sys
import csv
import os
import json

def main(inFileFac, trnsDept,
			trnsAffs, targetDir):
	if not os.path.exists(targetDir):
		os.makedirs(targetDir)

	depts = dict()
	affs = dict()
	facs = []

	with open(trnsDept, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
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

	with open(trnsAffs, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		# facid, deptid, rank(?)
		for row in rdr:
			# Only interested in positions ranked 1
			# This also skips unranked positions (val=0)
			if row[2] != '1':
				print row
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

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])