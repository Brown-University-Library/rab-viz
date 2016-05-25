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
			os.path.join(targetDir,'viz_force_dept_data.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		for dept in deptLegend:
			pagedLegend = deptLegend[dept]
			for page, legend in enumerate(pagedLegend):
				links = []
				for f in legend:
					fdct = coauthData[f]
					for co in fdct.keys():
						# Conditional needed for coauthor's coauthors,
						# who may not be present in the legend
						if co in legend:
							link = {
								"source": legend.index(f),
								"target": legend.index(co),
								"value": fdct[co]
							}
							links.append(link)
				row = [ dept, page, json.dumps(legend), json.dumps(links) ]
				wrtr.writerow(row)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3])