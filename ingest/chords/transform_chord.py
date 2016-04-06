from collections import defaultdict
import json
import csv

cnt = defaultdict(lambda : defaultdict(dict))
rcnt = defaultdict(lambda : defaultdict(dict))
depts = dict()
mtxs = []

# Medicine
target_dept = "http://vivo.brown.edu/individual/org-brown-univ-dept84"

with open("data_in/medicine_nx.csv", "r") as f:
	rdr = csv.reader(f, delimiter=',', quotechar='"')
	#Skip header
	head = rdr.next()
	#Auth1, Auth2, Num/Coauths, Dept/Auth2
	for row in rdr:
		cnt[row[0]][row[1]] = int(row[2])
		rcnt[row[1]][row[0]] = int(row[2])
		depts[row[1]] = row[3]

# Necessary for SPARQL query anomalies
for k, v in rcnt.items():
	if k in cnt:
		continue
	else:
		cnt[k] = v

with open('data_out/chord_data.csv', 'w') as dataout:
	wrtr = csv.writer(dataout)
	rabids = []
	g = cnt.keys()
	mtx = [[0 for x in range(len(g))] for x in range(len(g))] 
	for f in g:
		fdct = cnt[f]
		authDept = depts.get(f, target_dept)
		for co in fdct.keys():
			mtx[g.index(f)][g.index(co)] = fdct[co]
		rabids.append([f, authDept])
	row = [ target_dept, json.dumps(rabids), json.dumps(mtx) ]
	wrtr.writerow(row)