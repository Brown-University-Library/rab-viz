import sys
import csv
import os
import json
from collections import defaultdict

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
			os.path.join(targetDir,'viz_force_fac_data.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		for fac in legends:
			links = []
			legend = legends[fac]
			for f in legend:
				fdct = coauthData[f]
				for co in fdct.keys():
					if co in legend: # AuthJson dicts not limited to this dept
						link = {
							"source": legend.index(f),
							"target": legend.index(co),
							"value": fdct[co]
						}
					links.append(link)
			row = [ fac, 0, json.dumps(legend), json.dumps(links) ]
			wrtr.writerow(row)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])