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
		deptNet = []
		for fac in rosters[dept]:
			deptNet.extend(coauthData[fac].keys())
			deptNet.append(fac)
		deptLegend[dept] = list(set(deptNet))

	with open(
			os.path.join(targetDir,'chordDeptViz_data.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		for dept in deptLegend:
			fullLegend = deptLegend[dept]
			# http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
			if len(fullLegend) > 20:
				pagedLegend = [fullLegend[i:i+20] for i in xrange(0, len(fullLegend), 20)]
				pagedLegend.insert(0,fullLegend)
			else:
				pagedLegend = [fullLegend]
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