from collections import defaultdict
import json
import csv
import networkx as nx

cnt = defaultdict(lambda : defaultdict(dict))
rcnt = defaultdict(lambda : defaultdict(dict))
pool = nx.Graph()
mtxs = []

# def pool_coauths(pools):
# 	print len(pools), "\n\n"
# 	for p in pools:
# 		print len(pools[p])
# 	poolList = list({ frozenset(pools[p]) for p in pools })
# 	print poolList[0]
# 	print poolList[1]
# 	blob = reduce(lambda a, b: a.union(b), poolList[0], poolList[1:])
# 	return blob


with open("data_in/medicine_nx.csv", "r") as f:
	rdr = csv.reader(f, delimiter=',', quotechar='"')
	#Skip header
	head = rdr.next()
	for row in rdr:
		cnt[row[0]][row[1]] = int(row[2])
		rcnt[row[1]][row[0]] = int(row[2])
		pool.add_edge(row[0],row[1])

for k, v in rcnt.items():
	if k in cnt:
		continue
	else:
		cnt[k] = v

# ntx = pool_coauths(pools)
graphId = 0
facVizAssc = []

with open('data_out/chord_data.csv', 'w') as dataout:
	wrtr = csv.writer(dataout)
	for ntwk in nx.connected_components(pool):
		g = list(ntwk)
		print g
		graphId += 1
		rabids = []
		mtx = [[0 for x in range(len(g))] for x in range(len(g))] 
		for f in g:
			fdct = cnt[f]
			for co in fdct.keys():
				mtx[g.index(f)][g.index(co)] = fdct[co]
			rabids.append(f)
			facVizAssc.append((f,graphId))
		out = {"key": rabids, "data": mtx}
		wrtr.writerow(json.dumps(out))

with open('data_out/fac_data.csv', 'w') as facout:
	wrtr = csv.writer(facout)
	wrtr.writerows(facVizAssc)