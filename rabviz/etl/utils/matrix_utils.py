def build_matrix_from_graph(graph):
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