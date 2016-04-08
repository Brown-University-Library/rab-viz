from collections import defaultdict
import json
import csv

cnt = defaultdict(lambda : defaultdict(dict))
rcnt = defaultdict(lambda : defaultdict(dict))
depts = dict()
mtxs = []

with open("data_in/all_coauths.csv", "r") as f:
	rdr = csv.reader(f, delimiter=',', quotechar='"')
	#Skip header
	head = rdr.next()
	#Auth1, Auth2, Num/Coauths, Dept/Auth2
	for row in rdr:
		cnt[row[0]][row[1]] = int(row[2])
		rcnt[row[1]][row[0]] = int(row[2])

# Necessary for SPARQL query anomalies
for k, v in rcnt.items():
	if k in cnt:
		continue
	else:
		cnt[k] = v

with open('data_out/fac_chord_data.csv', 'w') as dataout:
	wrtr = csv.writer(dataout)
	for auth in cnt:
		rabids = []
		rabids.append(auth)
		coauths = cnt[auth].keys()
		rabids.extend(coauths)
		for coauth in coauths:
			cocoauths = cnt[coauth].keys()
			rabids.extend(cocoauths)
		rabids = list(set(rabids))
		rabids.insert(0, rabids.pop(rabids.index(auth)))
		mtx = [[0 for x in range(len(rabids))] for x in range(len(rabids))]
		for f in rabids:
			fdct = cnt[f]
			for co in fdct.keys():
				try:
					mtx[rabids.index(f)][rabids.index(co)] = fdct[co]
				except:
					continue
		row = [auth, json.dumps(rabids), json.dumps(mtx)]
		wrtr.writerow(row)