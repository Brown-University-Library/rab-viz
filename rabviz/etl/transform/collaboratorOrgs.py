import networkx
from etl.utils import data_utils, graph_utils

collection_name = 'collaborators'
key_field = 'rabid'
value_field = 'graph'
input_files = ['faculty.csv', 'collaborators.csv',
    'affiliations.csv', 'departments.csv']

def key_graph_by_node_group(groupNodesIndex):
    def data_func(group, graph):
        merged_graph = networkx.DiGraph()
        for node in groupNodesIndex[group]:
            subgraph = graph_utils.get_subgraph_by_node(graph, node, depth=1)
            merged_graph = networkx.compose(merged_graph, subgraph)
        for node in groupNodesIndex[group]:
            merged_graph.nodes[node]['level'] = 0
        data = networkx.node_link_data(merged_graph)
        cleaned = graph_utils.clean_null_graph(data)
        return cleaned
    return data_func

def transform(facultyData, collaboratorData,
        affiliationsData, departmentData):
    faculty_attrs = [ data_utils.row_reducer(row, [0,3,5,4])
        for row in facultyData ]
    with_level = [ row + [1] for row in faculty_attrs ]
    fac_attrs_index = data_utils.data_indexer(with_level, 0, pop=True)
    labelled_index = { 
        fac: data_utils.data_labeller(attr, ['name','group','title','level'])
            for fac, attr in fac_attrs_index.items() }
    collab_graph = graph_utils.build_graph_from_rows(
        nodeRows=with_level, edgeRows=collaboratorData,
        weighted=False, directed=True)
    graph_with_attrs = graph_utils.add_node_attributes(collab_graph,
        labelled_index)

    affiliations = [ data_utils.row_reducer(row, [0,1])
        for row in affiliationsData ]
    departments  = [ row[0] for row in departmentData ]
    affiliations_index = { dept: [ row[0] 
        for row in data_utils.data_filter(affiliations, 1, dept) ]
            for dept in departments }
    gnrtr =  data_utils.data_generator(
        departments, graph_with_attrs, key_graph_by_node_group(affiliations_index))
    return gnrtr