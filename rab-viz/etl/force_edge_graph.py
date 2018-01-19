import networkx
import csv
import json
from collections import defaultdict
import os

with open('coauthors.csv','r') as c:
	rdr = csv.reader(c)
	header = next(rdr)
	coauths = [ row for row in rdr ]

with open('faculty.csv','r') as f:
	rdr = csv.reader(f)
	header = next(rdr)
	fac_data = { row[0] : { 'name' : row[3], 'dept': row[5] } for row in rdr }

wx = defaultdict(networkx.Graph)
for co in coauths:
	if wx[co[0]].has_edge(co[0],co[1]):
		wx[co[0]][co[0]][co[1]]['weight'] += 1
	else:
		wx[co[0]].add_edge(co[0],co[1], weight=1)

sumx = dict()
for fac in wx:
	g = wx[fac].copy()
	nds = list(g.nodes)
	# nds.remove(fac)
	for n in nds:
		co_g = wx[n]
		g = networkx.compose(g, co_g)
	sumx[fac] = g
	new_nodes = list(sumx[fac].nodes)
	for w in new_nodes:
		sumx[fac].add_node(w, group=fac_data[w]['dept'], name=fac_data[w]['name'])

html = """
<html>
	<head>
		<style>
			h3 {{
				margin-bottom: 0;
			}}
			ul {{
				margin-top: 0;
				list-style-type: none;
			}}
			dt, dd {{
				display: inline;
			}}
		</style>
	</head>
	<body>
		{0}
	</body>
</html>
"""

target = "file://{0}/edge_graph.html".format( os.path.abspath('.') )
link = """
	<h3>
		<a href="edge_graph.html?faculty={1}">{2}</a>
	</h3>
	<ul>
		<li>
			<dl>
				<dt>Local</dt>
				<dd>{3}</dd>
			</dl>
		</li>
		<li>
			<dl>
				<dt>Extended</dt>
				<dd>{4}</dd>
			</dl>
		</li>
	</ul>	
"""
links = "\n".join(
	[ link.format( target, shortid[33:], sumx[shortid].node[shortid]['name'],
		len(wx[shortid]), len(sumx[shortid])) for shortid in sumx ])
with open('index.html', 'w') as gdx:
	gdx.write(html.format(links))

for fac_g in sumx:
	shortid = fac_g[33:]
	g = sumx[fac_g]
	with open('data/' + shortid + '.json', 'w') as out:
		data = networkx.node_link_data(g)
		json.dump(data, out)