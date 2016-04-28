import sys
import csv
import os

def main(inFile, targetDir):
	if not os.path.exists(targetDir):
		os.makedirs(targetDir)

	affs = []

	with open(inFile, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		#Skip header
		head = rdr.next()
		#facid, deptid, rank
		for row in rdr:
			# Some positions don't have ranks!!!
			if not row[2]:
				rank = 0
			else:
				rank = row[2]
			affs.append((row[0], row[1], rank))

	with open(
			os.path.join(targetDir,'affiliations_data.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		wrtr.writerows(affs)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])