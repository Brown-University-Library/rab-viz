from collections import defaultdict
import sys
import csv
import os
import json

def main(inFileAuthJson, targetDir):
	if not os.path.exists(targetDir):
		os.makedirs(targetDir)

	coauthData = dict()
	nx2 = defaultdict(set)

	with open(inFileAuthJson, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		for row in rdr:
			coauthData[row[0]] = json.loads(row[1])

	for auth in coauthData:
		nx2[auth].add(auth)
		for coauth in coauthData[auth]:
			nx2[auth].add(coauth)
			cocoauths = coauthData[coauth].keys()
			nx2[auth].update(cocoauths)

	legends = { auth: list(nx2[auth]) for auth in nx2 }

	with open(
			os.path.join(targetDir,'chordFacViz_data.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		for fac in legends:
			legend = legends[fac]
			mtx = [[0 for x in range(len(legend))] for x in range(len(legend))] 
			for f in legend:
				fdct = coauthData[f]
				for co in fdct.keys():
					if co in legend:
						mtx[legend.index(f)][legend.index(co)] = fdct[co]
			row = [ fac, json.dumps(legend), json.dumps(mtx) ]
			wrtr.writerow(row)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])