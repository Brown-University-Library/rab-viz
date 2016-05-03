import sys
import csv
import os
import json

def main(inFileFac, targetDir):
	if not os.path.exists(targetDir):
		os.makedirs(targetDir)

	facs = []

	with open(inFileFac, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		#Skip header
		head = rdr.next()
		# rabid, last, first, label, title, primaryOU 
		for row in rdr:
			if not row[5]:
				primaryOU = "None"
			else:
				primaryOU = row[5]
			facs.append((row[0], row[1], row[2], row[3], row[4], primaryOU))

	with open(
			os.path.join(targetDir,'faculty_data.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		for fac in facs:
			rabid, last, first, name, title, ou = fac
			abbrev = last + ", " + first[0]
			row = (rabid, last, first, name, abbrev, title, ou)
			wrtr.writerow(row)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])