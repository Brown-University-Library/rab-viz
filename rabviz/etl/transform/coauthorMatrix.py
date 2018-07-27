import networkx
from transform import utils

collection_name = 'coauthors'
key_field = 'rabid'
value_field = 'matrix'
input_files = ['faculty.csv', 'coauthors.csv']

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

def add_node_attributes(graph, node_attribute_lookup):
    nodes = [ n for n in graph.nodes() ]
    nodes_with_attrs = [ node_attribute_lookup[n] for n in nodes ]
    for n in nodes_with_attrs:
        graph.add_node(n[0], name=n[1], group=n[2])
    return graph

def build_matrix(graph):
    nodes_data = [ { 'id': n[0], 'name': n[1]['name'],
                    'group': n[1]['group'] } for n in graph.nodes.data() ]
    nodes = [ n['id'] for n in nodes_data ]
    matrix = [ [ 0 for x in range( len(nodes) ) ]
                    for x in range( len(nodes) ) ]
    for focus_idx, focus in enumerate(nodes):
        for node, attrs in graph[focus].items():
            node_idx = nodes.index(node)
            matrix[focus_idx][node_idx] = attrs['weight']
    data = { 'nodes': nodes_data, 'matrix': matrix }
    return data

def key_coauth_matrix(node, graph):
    subgraph = get_subgraph_by_node(graph, node)
    data = build_matrix(subgraph)
    return data

def transform(facultyData, coauthorData):
    faculty_attrs = [ utils.row_reducer(row, [0,3,5]) for row in facultyData ]
    faculty_index = utils.data_indexer(faculty_attrs, 0)
    coauth_graph = build_total_graph(coauthorData)
    graph_with_attrs = add_node_attributes(coauth_graph, faculty_index)
    faculty_list = [ n for n in graph_with_attrs.nodes() ]
    gnrtr =  utils.data_generator(
        faculty_list, graph_with_attrs, key_coauth_matrix)
    return gnrtr