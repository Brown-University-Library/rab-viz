import networkx

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
        graph.add_node(n[0], name=n[1], group=n[2], title=n[3])
    return graph

def build_directed_graph(data):
    graph = networkx.DiGraph()
    for row in data:
        graph.add_edge(row[0],row[1], weight=1)
    return graph