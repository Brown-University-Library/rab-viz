import networkx
from utils import data_utils, graph_utils

collection_name = 'collaborators'
key_field = 'rabid'
value_field = 'graph'
input_files = ['faculty.csv', 'collaborators.csv']

def key_graph_by_node(node, graph):
    subgraph = graph_utils.get_subgraph_by_node(graph, node, track_depth=True)
    data = networkx.node_link_data(subgraph)
    return data

def transform(facultyData, collaboratorData):
    faculty_attrs = [ data_utils.row_reducer(row, [0,3,5,4])
        for row in facultyData ]
    fac_attrs_index = data_utils.data_indexer(faculty_attrs, 0, pop=True)
    labelled_index = { 
        fac: data_utils.data_labeller(attr, ['name','group','title'])
            for fac, attr in fac_attrs_index.items() }
    collab_graph = graph_utils.build_graph_from_rows(
        edgeRows=collaboratorData,
        weighted=False, directed=True)
    graph_with_attrs = graph_utils.add_node_attributes(collab_graph,
        labelled_index)
    faculty_list = [ n for n in graph_with_attrs.nodes() ]
    gnrtr =  data_utils.data_generator(
        faculty_list, graph_with_attrs, key_graph_by_node)
    return gnrtr