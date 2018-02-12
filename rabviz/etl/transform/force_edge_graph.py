import networkx
import csv
import json
import os
import pymongo
import json

from config.settings import config


def unique_on_fields(data, fields=[]):
    wrapped = [ (frozenset([ row[field] for field in fields ]), row)
                    for row in data ]
    checked = set()
    filtered = []
    for w in wrapped:
        if w[0] in checked:
            continue
        else:
            filtered.append(w[1])
            checked.add(w[0])
    return filtered

def build_total_graph(data):
    graph = networkx.Graph()
    unique_data = unique_on_fields(data, [0,1,2])
    for row in unique_data:
        if graph.has_edge(row[0], row[1]):
            graph[row[0]][row[1]]['weight'] += 1
        else:
            graph.add_edge(row[0],row[1], weight=1)
    return graph

def get_subgraph_by_node(graph, node, depth=2):
    nodes = { node }
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

def add_node_attributes(graph, node_attribute_lookup):
    nodes = [ n for n in graph.nodes() ]
    nodes_with_attrs = [ node_attribute_lookup[n] for n in nodes ]
    for n in nodes_with_attrs:
        graph.add_node(n[0], name=n[1], group=n[2])
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

    faculty_list = [ n for n in graph_with_attrs.nodes() ]
    mongo_client = pymongo.MongoClient('localhost', 27017)
    viz_db = mongo_client.get_database('rabviz')
    viz_coll = viz_db['forceEdge']
    for f in faculty_list:
        subgraph = get_subgraph_by_node(graph_with_attrs, f)
        data = networkx.node_link_data(subgraph)
        viz_coll.replace_one({ 'rabid': f },
            { 'rabid': f, 'data': data }, True)
        # shortid = f[33:]
        # destination = os.path.join(graphDir, shortid + '.json')
        # with open(destination, 'w') as out:
        #     data = networkx.node_link_data(subgraph)
        #     json.dump(data, out)

if __name__ == "__main__":
    main()