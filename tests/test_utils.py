import unittest
import context

import networkx

from rabviz.etl.utils import graph_utils, data_utils

class TestDataUtils(unittest.TestCase):

    def test_data_labeller(self):
        data = [ 1, 'foo', 'bar' ]
        labels = [ 'id', 'name', 'group' ]
        labelled = data_utils.data_labeller(data, labels)
        self.assertEqual(labelled,
            {'id': 1, 'name': 'foo', 'group': 'bar' })

    def test_unique_on_fields(self):
        data = [ [ 1,2,'a' ], [ 2,1,'b' ], [ 2,1,'a' ] ]
        filtered = data_utils.unique_on_fields(data, [0,1,2])
        self.assertEqual(len(filtered), 2)
        self.assertIn( [1,2,'a'], filtered )
        self.assertNotIn( [2,1,'a'], filtered )


class TestGraphUtils(unittest.TestCase):

    def test_build_graph_from_rows(self):
        data = [ [ 1, 2, 'a' ], [ 2, 1, 'b' ], [ 2, 1, 'a' ],
                    [ 1, 3, 'c' ], [ 4, 5, 'd' ] ]
        graph  = graph_utils.build_graph_from_rows(data)
        self.assertIn( 1, graph )
        self.assertIn( 5, graph )
        self.assertEqual( graph[1][2]['weight'], 3)
        self.assertEqual( graph[3][1]['weight'], 1)

        unique = data_utils.unique_on_fields(data, [0,1,2])
        graph  = graph_utils.build_graph_from_rows(unique)
        self.assertIn( 1, graph )
        self.assertIn( 5, graph )
        self.assertEqual( graph[1][2]['weight'], 2)
        self.assertEqual( graph[3][1]['weight'], 1)

    def test_get_subgraph_by_node(self):
        data = [ [ 1, 2, 'a' ], [ 2, 1, 'b' ], [ 2, 1, 'a' ],
                    [ 1, 3, 'c' ], [ 4, 5, 'd' ] ]
        graph = graph_utils.build_graph_from_rows(data)
        subgraph = graph_utils.get_subgraph_by_node(graph, 1)
        self.assertIn( 1, graph )
        self.assertIn( 5, graph )
        self.assertIn( 1, subgraph )
        self.assertNotIn( 5, subgraph )
        self.assertIsInstance( subgraph, networkx.Graph )

        graph = graph_utils.build_graph_from_rows(data, directed=True)
        subgraph = graph_utils.get_subgraph_by_node(graph, 1)
        self.assertIsInstance( subgraph, networkx.DiGraph )

    def test_add_node_attributes(self):
        data = [ [ 1, 2, 'a' ], [ 2, 1, 'b' ], [ 2, 1, 'a' ] ]
        attributes = {
            1: { 'group':'foo', 'name':'bar'},
            2: { 'group':'baz', 'name':'bot'}
        }

        graph = graph_utils.build_graph_from_rows(data)
        graph_attr = graph_utils.add_node_attributes(graph, attributes)
        self.assertEqual(graph_attr.node[1]['group'], 'foo')
        self.assertEqual(graph_attr.node[1]['name'], 'bar')
        self.assertEqual(graph_attr.node[2]['group'], 'baz')
        self.assertEqual(graph_attr.node[2]['name'], 'bot')

        data = [ [ 1, 2, 'a' ], [ 2, 1, 'b' ], [ 2, 1, 'a' ],
                    [ 1, 3, 'c' ] ]
        graph = graph_utils.build_graph_from_rows(data)
        with self.assertRaises(KeyError):
            graph_utils.add_node_attributes(graph, attributes)

if __name__ == "__main__":
    unittest.main()