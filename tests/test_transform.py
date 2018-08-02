import unittest
import context

from rabviz.etl.utils import graph_utils

class TestGraphTransform(unittest.TestCase):

    def test_unique_on_fields(self):
        data = [ [ 1,2,'a' ], [ 2,1,'b' ], [ 2,1,'a' ] ]
        filtered = graph_utils.unique_on_fields(data, [0,1,2])
        self.assertEqual(len(filtered), 2)
        self.assertIn( [1,2,'a'], filtered )
        self.assertNotIn( [2,1,'a'], filtered )

    def test_build_total_graph(self):
        data = [ [ 1, 2, 'a' ], [ 2, 1, 'b' ], [ 2, 1, 'a' ],
                    [ 1, 3, 'c' ], [ 4, 5, 'd' ] ]
        graph  = graph_utils.build_total_graph(data)
        self.assertIn( 1, graph )
        self.assertIn( 5, graph )
        self.assertEqual( graph[1][2]['weight'], 2)
        self.assertEqual( graph[3][1]['weight'], 1)

    def test_get_subgraph_by_node(self):
        data = [ [ 1, 2, 'a' ], [ 2, 1, 'b' ], [ 2, 1, 'a' ],
                    [ 1, 3, 'c' ], [ 4, 5, 'd' ] ]
        graph = graph_utils.build_total_graph(data)
        subgraph = graph_utils.get_subgraph_by_node(graph, 1)
        self.assertIn( 1, graph )
        self.assertIn( 5, graph )
        self.assertIn( 1, subgraph )
        self.assertNotIn( 5, subgraph )

    def test_add_node_attributes(self):
        data = [ [ 1, 2, 'a' ], [ 2, 1, 'b' ], [ 2, 1, 'a' ] ]
        graph = graph_utils.build_total_graph(data)
        attributes = { 1: [1, 'foo', 'bar'], 2: [2, 'baz', 'bot'] }
        graph_attr = graph_utils.add_node_attributes(graph, attributes)
        self.assertEqual(graph_attr.node[1]['group'], 'foo')
        self.assertEqual(graph_attr.node[1]['name'], 'bar')
        self.assertEqual(graph_attr.node[2]['group'], 'baz')
        self.assertEqual(graph_attr.node[2]['name'], 'bot')

        data = [ [ 1, 2, 'a' ], [ 2, 1, 'b' ], [ 2, 1, 'a' ],
                    [ 1, 3, 'c' ] ]
        graph = graph_utils.build_total_graph(data)
        attributes = { 1: [1, 'foo', 'bar'], 2: [2, 'baz', 'bot'] }
        with self.assertRaises(KeyError):
            graph_utils.add_node_attributes(graph, attributes)

if __name__ == "__main__":
    unittest.main()