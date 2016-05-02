from collections import defaultdict
import sys
import csv
import os
import json

def main(inFileAuthJson, inFileRosters, targetDir):
	if not os.path.exists(targetDir):
		os.makedirs(targetDir)

	rosters = dict()
	coauthData = dict()
	ntx = dict()
	matrixes = []

	with open(inFileAuthJson, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		for row in rdr:
			coauthData[row[0]] = json.loads(row[1])

	with open(inFileRosters, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		for row in rdr:
			coauths = set()
			for fac in json.loads(row[1]):
				if fac in coauthData:
					coauths.add(fac)
			rosters[row[0]] = list(coauths)

	for r in rosters:
		print r, "\t", len(rosters[r])

	# with open(inFileFac, "r") as f:
	# 	rdr = csv.reader(f, delimiter=',', quotechar='"')
	# 	for row in rdr:
	# 		facs[row[0]] = row

	# with open(inFileAffs, "r") as f:
	# 	rdr = csv.reader(f, delimiter=',', quotechar='"')
	# 	for row in rdr:
	# 		# Only look up active faculty
	# 		if facs.get(row[0]):
	# 			affs[row[1]].add(row[0])

	# for dept, facSet in affs.items():
	# 	coauths = set()
	# 	cnt = 0
	# 	print dept
	# 	for fac in facSet:
	# 		cnt +=1
	# 		print cnt, fac
	# 		coauths.add(fac)
	# 		print "\t",authjson[fac].keys(), len(authjson[fac].keys())
	# 		for k in authjson[fac].keys():
	# 			coauths.add(k)
	# 	print coauths, len(coauths)
	# 		# coauths.update(json.loads(authjson[fac]).keys())
	# 	ntx[dept] = list(coauths)

	# with open(
	# 		os.path.join(targetDir,'chordDeptViz.csv'),
	# 		 'w') as dataout:
	# 	wrtr = csv.writer(dataout)
	# 	for dept in ntx:
	# 		# print dept
	# 		# print ntx[dept]
	# 		facList = ntx[dept]
	# 		mtx = [[0 for x in range(len(facList))] for x in range(len(facList))] 
	# 		for f in facList:
	# 			fdct = authjson[f]
	# 			# print f
	# 			# print fdct
	# 			for co in fdct.keys():
	# 				mtx[facList.index(f)][facList.index(co)] = fdct[co]
	# 		row = [ dept, json.dumps(facList), json.dumps(mtx) ]
	# 		wrtr.writerow(row)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3])