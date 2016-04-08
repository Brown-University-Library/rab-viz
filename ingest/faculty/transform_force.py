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
	#Auth1, Auth2, Num/Coauths
	for row in rdr:
		cnt[row[0]][row[1]] = int(row[2])
		rcnt[row[1]][row[0]] = int(row[2])

for k, v in rcnt.items():
	if k in cnt:
		continue
	else:
		cnt[k] = v

with open('data_out/fac_force_data.csv', 'w') as dataout:
	wrtr = csv.writer(dataout)
	for auth in cnt:
		rabids = []
		data = []
		rabids.append(auth)
		coauths = cnt[auth].keys()
		rabids.extend(coauths)
		for coauth in coauths:
			cocoauths = cnt[coauth].keys()
			rabids.extend(cocoauths)
		rabids = list(set(rabids))
		for f in rabids:
			fdct = cnt[f]
			for co in fdct.keys():
				try:
					link = {
							"source": rabids.index(f),
							"target": rabids.index(co),
							"value": fdct[co]
							}
				except:
					continue
				data.append(link)
		row = [auth, json.dumps(rabids), json.dumps(data)]
		wrtr.writerow(row)