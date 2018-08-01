import networkx
from transform import utils

collection_name = 'collaborators'
key_field = 'rabid'
value_field = 'graph'
input_files = ['faculty.csv', 'collaborators.csv',
    'affiliations.csv', 'departments.csv']

def build_total_graph(nodeData, edgeData):
    graph = networkx.DiGraph()
    for row in nodeData:
        graph.add_node(
            graph.add_node(row[0], name=row[1], group=row[2], title=row[3]) )
    for row in edgeData:
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

def key_graph_by_node_group(groupNodesIndex):
    def data_func(group, graph):
        merged_graph = networkx.DiGraph()
        for node in groupNodesIndex[group]:
            subgraph = get_subgraph_by_node(graph, node, depth=1)
            merged_graph = networkx.compose(merged_graph, subgraph)
        data = networkx.node_link_data(merged_graph)
        return data
    return data_func

def transform(facultyData, collaboratorData,
        affiliationsData, departmentData):
    faculty = [ utils.row_reducer(row, [0,3,5,4]) for row in facultyData ]
    affiliations = [ utils.row_reducer(row, [0,1]) for row in affiliationsData ]
    departments  = [ row[0] for row in departmentData ]
    collab_graph = build_total_graph(faculty, collaboratorData)
    affiliations_index = { dept: [ row[0] 
        for row in utils.data_filter(affiliations, 1, dept) ]
            for dept in departments }
    gnrtr =  utils.data_generator(
        departments, collab_graph, key_graph_by_node_group(affiliations_index))
    return gnrtr
