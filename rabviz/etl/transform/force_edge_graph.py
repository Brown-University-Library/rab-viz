import networkx
import csv
import json
from collections import defaultdict
import os

from config.settings import config


def build_total_graph(rows):
    graph = networkx.Graph()
    for row in rows:
        if graph.has_edge(row[0], row[1]):
            graph[row[0]][row[1]]['weight'] += 1
        else:
            graph.add_edge(row[0],row[1], weight=1)
    return graph

def get_individual_faculty_graph(graph, faculty_uri, depth=2):
    nodes = { faculty_uri }
    for d in range(depth):
        for n in nodes:
            neighbors = { b for b in iter(graph[n]) }
            nodes = nodes | neighbors
    subgraph = networkx.Graph(graph.subgraph(nodes))
    return subgraph

def row_reducer(row, indexer=[]):
    return [ row[i] for i in indexer ]

def data_indexer(data, index=0):
    return { row[index] : row for row in data }

def add_node_attributes(graph, attribute_map):
    faculty = [ f for f in graph.nodes() ]
    faculty_attrs = [ attribute_map[f] for f in faculty ]
    for f in faculty_attrs:
        graph.add_node(f[0], group=f[1], name=f[2])
    return graph

def main():
    extractDir = os.path.join(config['DATA_DIR'],'extract')
    graphDir = os.path.join(
        config['DATA_DIR'], 'transform', 'force_edge_graphs')

    with open( os.path.join(extractDir,'coauthors.csv'), 'r' ) as c:
        rdr = csv.reader(c)
        header = next(rdr)
        coauth_data = [ row for row in rdr ]

    with open( os.path.join(extractDir,'faculty.csv'), 'r' ) as f:
        rdr = csv.reader(f)
        header = next(rdr)
        fac_data = [ row for row in rdr ]

    faculty_attrs = [ row_reducer(row, [0,3,5]) for row in fac_data ]
    faculty_index = data_indexer(faculty_attrs, 0)

    coauth_graph = build_total_graph(coauth_data)
    graph_with_attrs = add_node_attributes(coauth_graph, faculty_index)

    faculty_list = { row_reducer(row, [0])[0] for row in coauth_data }
    for f in faculty_list:
        subgraph = get_individual_faculty_graph(graph_with_attrs, f)
        shortid = f[33:]
        destination = os.path.join(graphDir, shortid + '.json')
        with open(destination, 'w') as out:
            data = networkx.node_link_data(subgraph)
            json.dump(data, out)

if __name__ == "__main__":
    main()