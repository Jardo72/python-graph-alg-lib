#
# Copyright 2020 Jaroslav Chmurny
#
# This file is part of Library of Graph Algorithms for Python.
#
# Library of Graph Algorithms for Python is free software developed for
# educational # and experimental purposes. It is licensed under the Apache
# License, Version 2.0 # (the "License"); you may not use this file except
# in compliance with the # License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Unit tests for the graphlib.util module.
"""

from io import StringIO

from pytest import mark

from graphlib.dump import dump_graph, dump_shortest_path
from graphlib.graph import AdjacencySetGraph, GraphType
from graphlib.algorithms import Edge, ShortestPathSearchResult

class TestGumpGraph: # pylint: disable=R0201,C0116
    
    @mark.skip('Test case not implemented yet')
    def test_graph_is_dumped_properly_for_directed_weighted_graph(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'B', 3)
        graph.add_edge('A', 'C', 2)
        graph.add_edge('B', 'D', 5)
        graph.add_edge('C', 'D', 4)

        with StringIO() as output:
            dump_graph(graph, output)
            result = output.getvalue()
        
        assert result == """
Graph type: GraphType.DIRECTED
Weighted: YES
Vertices (totally 4):
 - A
 - B
 - C
 - D
 Edges:
 - A -> B (weight = 3)
 - A -> C (weight = 2)
 - B -> D (weight = 5)
 - C -> D (weight = 4)
 """

    @mark.skip('Test case not implemented yet')
    def test_graph_is_dumped_properly_for_undirected_unweighted_graph(self):
        graph = AdjacencySetGraph(GraphType.UNDIRECTED)
        graph.add_edge('', '')
        graph.add_edge('', '')
        graph.add_edge('', '')
        graph.add_edge('', '')
        graph.add_edge('', '')

        with StringIO() as output:
            dump_graph(graph, output)
            result = output.getvalue()
        
        assert result == """
Graph type: GraphType.UNDIRECTED
Weighted: NO
Vertices (totally 4):
 - A
 - B
 - C
 - D
 Edges:
 - A -> B (weight = 3)
 - A -> C (weight = 2)
 - B -> D (weight = 5)
 - C -> D (weight = 4)
"""


class TestDumpShortestPath: # pylint: disable=R0201,C0116

    def test_shortest_path_is_dumped_properly(self):
        path = (
            Edge(start='A', destination='B', weight=3),
            Edge(start='B', destination='C', weight=2),
            Edge(start='C', destination='D', weight=5),
        )
        shortest_path = ShortestPathSearchResult(path)

        with StringIO() as output:
            dump_shortest_path(shortest_path, output)
            result = output.getvalue()
        
        assert result == """
Shortest path from A to D
Overall distance 10
Path:
 - A -> B (weight = 3)
 - B -> C (weight = 2)
 - C -> D (weight = 5)
"""
