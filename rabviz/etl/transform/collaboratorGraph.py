import networkx
from transform import utils

collection_name = 'collaborators'
key_field = 'rabid'
value_field = 'graph'
input_files = ['faculty.csv', 'collaborators.csv']

def build_total_graph(data):
    graph = networkx.DiGraph()
    for row in data:
        graph.add_edge(row[0],row[1], weight=1)
    return graph

def get_subgraph_by_node(graph, node, depth=2):
    nodes = { node }
    for d in range(depth):
        for n in nodes:
            neighbors = { b for b in iter(graph[n]) }
            nodes = nodes | neighbors
    subgraph = networkx.DiGraph(graph.subgraph(nodes))
    return subgraph

def add_node_attributes(graph, node_attribute_lookup):
    nodes = [ n for n in graph.nodes() ]
    nodes_with_attrs = [ node_attribute_lookup[n] for n in nodes ]
    for n in nodes_with_attrs:
        graph.add_node(n[0], name=n[1], group=n[2], title=n[3])
    return graph

def key_graph_by_node(node, graph):
    subgraph = get_subgraph_by_node(graph, node)
    data = networkx.node_link_data(subgraph)
    return data

def transform(facultyData, collaboratorData):
    faculty_attrs = [ utils.row_reducer(row, [0,3,5,4]) for row in facultyData ]
    faculty_index = utils.data_indexer(faculty_attrs, 0)
    collab_graph = build_total_graph(collaboratorData)
    graph_with_attrs = add_node_attributes(collab_graph, faculty_index)
    faculty_list = [ n for n in graph_with_attrs.nodes() ]
    gnrtr =  utils.data_generator(
        faculty_list, graph_with_attrs, key_graph_by_node)
    return gnrtr
