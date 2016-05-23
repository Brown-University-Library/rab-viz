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
	deptLegend = dict()

	with open(inFileAuthJson, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		for row in rdr:
			coauthData[row[0]] = json.loads(row[1])

	with open(inFileRosters, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		for row in rdr:
			hasCoauths = set()
			for fac in json.loads(row[1]):
				if fac in coauthData:
					hasCoauths.add(fac)
			rosters[row[0]] = list(hasCoauths)

	rosters = { k: v for k, v in rosters.items()
					if len(v) !=0 }

	for dept in rosters:
		bigNet = []
		deptNet = []
		for fac in rosters[dept]:
			deptNet.extend(coauthData[fac].keys())
			deptNet.append(fac)
			if len(list(set(deptNet))) > 20:
				bigNet.append(list(set(deptNet)))
				deptNet = []
		if deptNet:
			bigNet.append(list(set(deptNet)))
		if len(bigNet) > 1:
			fullNet = list(
				{ name for net in bigNet for name in net }
				)
			bigNet.insert(0,fullNet)
		deptLegend[dept] = bigNet

	with open(
			os.path.join(targetDir,'viz_chord_dept_data.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		for dept in deptLegend:
			pagedLegend = deptLegend[dept]
			matrix = []
			for legend in pagedLegend:
				mtx = [[0 for x in range(len(legend))] for x in range(len(legend))] 
				for f in legend:
					fdct = coauthData[f]
					for co in fdct.keys():
						if co in legend: # AuthJson dicts not limited to this dept
							mtx[legend.index(f)][legend.index(co)] = fdct[co]
				matrix.append(mtx)
			row = [ dept, json.dumps(pagedLegend), json.dumps(matrix) ]
			wrtr.writerow(row)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3])