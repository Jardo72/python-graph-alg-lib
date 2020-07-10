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

"""Unit tests for the graphlib.algorithms module.
"""

from pytest import mark, raises

from graphlib.algorithms import Edge, ShortestPathSearchRequest, ShortestPathSearchResult
from graphlib.algorithms import find_shortest_path, sort_toplogically
from graphlib.graph import AdjacencySetGraph, GraphType


class TestTopologicalSort:

    def test_topological_sort_returns_vertices_in_proper_order(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('C', 'E')
        graph.add_edge('D', 'E')
        graph.add_edge('E', 'I')
        graph.add_edge('F', 'H')
        graph.add_edge('G', 'H')
        graph.add_edge('H', 'I')
        graph.add_edge('I', 'J')

        sort_result = sort_toplogically(graph)
        actual_order = list(sort_result)
        expected_order = ['A', 'B', 'D', 'F', 'G', 'C', 'H', 'E', 'I', 'J']
        assert expected_order == actual_order

    def test_attempt_to_apply_topological_sort_to_undirected_graph_leads_to_exception(self):
        graph = AdjacencySetGraph(GraphType.UNDIRECTED)
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('C', 'D')

        with raises(ValueError, match = r'.+ applied to directed graphs\.'):
            sort_toplogically(graph)

    def test_attepmt_to_apply_topological_sort_to_cyclic_graph_leads_to_exception(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('B', 'C')
        graph.add_edge('C', 'A')

        with raises(ValueError, match = r'.+ applied to acyclic graphs\.'):
            sort_toplogically(graph)


class TestShortestPath:

    def test_shortest_path_search_result_provides_proper_derived_properties(self):
        path = [
            Edge(start = 'A', destination = 'B', weight = 2),
            Edge(start = 'B', destination = 'C', weight = 3),
            Edge(start = 'C', destination = 'F', weight = 5),
            Edge(start = 'F', destination = 'H', weight = 2),
            Edge(start = 'H', destination = 'L', weight = 7),
        ]
        shortest_path = ShortestPathSearchResult(tuple(path))

        assert 'A' == shortest_path.start
        assert 'L' == shortest_path.destination
        assert 19 == shortest_path.overall_distance


    @mark.skip('Functionality not implemented yet')
    def test_shortest_path_search_finds_proper_shortest_path(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'B', 2)
        graph.add_edge('A', 'C', 4)
        graph.add_edge('A', 'D', 7)
        graph.add_edge('B', 'C', 1)
        graph.add_edge('D', 'C', 3)
        graph.add_edge('B', 'E', 5)
        graph.add_edge('C', 'F', 3)
        graph.add_edge('D', 'F', 8)
        graph.add_edge('E', 'F', 8)
        graph.add_edge('F', 'E', 5)
        graph.add_edge('E', 'G', 3)
        graph.add_edge('F', 'G', 2)

        search_request = ShortestPathSearchRequest(graph, start = 'A', destination = 'G')
        actual_search_result = find_shortest_path(search_request)

        path = [
            Edge(start = 'A', destination = 'B', weight = 2),
            Edge(start = 'B', destination = 'C', weight = 1),
            Edge(start = 'C', destination = 'F', weight = 3),
            Edge(start = 'F', destination = 'G', weight = 2),
        ]
        expected_search_result = ShortestPathSearchResult(tuple(path))
        assert expected_search_result == actual_search_result
