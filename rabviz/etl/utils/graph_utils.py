import networkx

def build_graph_from_rows(nodeRows=[], edgeRows=[],
        weighted=True, directed=False):
    if directed:
        graph = networkx.DiGraph()
    else:
        graph = networkx.Graph()
    for row in nodeRows:
        graph.add_node(row[0])
    for row in edgeRows:
        if graph.has_edge(row[0], row[1]) and weighted:
            graph[row[0]][row[1]]['weight'] += 1
        else:
            graph.add_edge(row[0],row[1], weight=1)
    return graph

def get_subgraph_by_node(graph, node, depth=2, track_depth=False):
    nodes = { node }
    tracker = { node: { 'level': 0 } }
    for d in range(depth):
        for n in nodes:
            neighbors = { b for b in iter(graph[n]) }
            for a in neighbors:
                if a not in tracker:
                    tracker[a] = { 'level' : d + 1 }
            nodes = nodes | neighbors
    if isinstance(graph, networkx.DiGraph):
        subgraph = networkx.DiGraph(graph.subgraph(nodes))
    else:
        subgraph = networkx.Graph(graph.subgraph(nodes))
    if track_depth:
        subgraph = add_node_attributes(subgraph, tracker)
    return subgraph

def add_node_attributes(graph, node_attribute_lookup):
    nodes = [ n for n in graph.nodes() ]
    for node in nodes:
        attrs = node_attribute_lookup[node]
        graph.add_node(node, **attrs)
    return graph

def clean_null_graph(data):
    if data['links'] == [] and len(data['nodes']) == 1:
        return {}
    else:
        return data