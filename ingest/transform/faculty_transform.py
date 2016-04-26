import sys
import csv
import os

def main(inFileFac, inFileAffs, targetDir):
	if not os.path.exists(targetDir):
		os.makedirs(targetDir)

	affs = dict()
	facs = []

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
				affs[row[0]] = row[1]
			else:
				affs[row[0]] = "Multiple"

	with open(
			os.path.join(targetDir,'faculty_data.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		for fac in facs:
			rabid, last, first, name, title = fac
			if affs.get(rabid):
				row = (rabid, last, first, name, title, affs[rabid])
			else:
				row = (rabid, last, first, name, title, "None")
			wrtr.writerow(row)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3])