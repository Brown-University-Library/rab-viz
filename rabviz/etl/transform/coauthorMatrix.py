import networkx
from etl.utils import data_utils, graph_utils, matrix_utils

collection_name = 'coauthors'
key_field = 'rabid'
value_field = 'matrix'
input_files = ['faculty.csv', 'coauthors.csv']

def key_coauth_matrix(node, graph):
    subgraph = graph_utils.get_subgraph_by_node(graph, node)
    data = matrix_utils.build_matrix_from_graph(subgraph)
    return data

def transform(facultyData, coauthorData):
    faculty_attrs = [ data_utils.row_reducer(row, [0,3,5])
        for row in facultyData ]
    fac_attrs_index = data_utils.data_indexer(faculty_attrs, 0, pop=True)
    labelled_index = { 
        fac: data_utils.data_labeller(attr, ['name','group'])
            for fac, attr in fac_attrs_index.items() }
    unique_coauthors = data_utils.unique_on_fields(coauthorData, [0,1,2])
    coauth_graph = graph_utils.build_graph_from_rows(
        edgeRows=unique_coauthors)
    graph_with_attrs = graph_utils.add_node_attributes(coauth_graph, labelled_index)
    faculty_list = [ n for n in graph_with_attrs.nodes() ]
    gnrtr =  data_utils.data_generator(
        faculty_list, graph_with_attrs, key_coauth_matrix)
    return gnrtr