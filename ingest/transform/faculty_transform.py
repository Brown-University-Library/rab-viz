import sys
import csv
import os

def main(inFileFac, inFileDept, inFileAffs, targetDir):
	if not os.path.exists(targetDir):
		os.makedirs(targetDir)

	depts = dict()
	affs = dict()
	facs = []

	with open(inFileDept, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		#Skip header
		head = rdr.next()
		#Auth1URI, Auth2URI, CitationURI
		for row in rdr:
			depts[row[0]] = row[1]

	with open(inFileFac, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		#Skip header
		head = rdr.next()
		#Auth1URI, Auth2URI, CitationURI
		for row in rdr:
			facs.append((row[0], row[1], row[2], row[3], row[4]))

	with open(inFileAffs, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		#Skip header
		head = rdr.next()
		#Auth1URI, Auth2URI, CitationURI
		for row in rdr:
			if not affs.get(row[0]):
				if depts.get(row[1]):
					affs[row[0]] = depts[row[1]]
				else:
					affs[row[0]] = "Other"
			else:
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