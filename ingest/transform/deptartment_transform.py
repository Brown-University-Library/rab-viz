import sys
import csv
import os

def main(inFile, targetDir):
	if not os.path.exists(targetDir):
		os.makedirs(targetDir)

	depts = []

	with open(inFile, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		#Skip header
		head = rdr.next()
		#Auth1URI, Auth2URI, CitationURI
		for row in rdr:
			depts.append((row[0], row[1]))

	with open(
			os.path.join(targetDir,'departments_data.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		wrtr.writerows(affs)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])