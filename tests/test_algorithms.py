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
from graphlib.algorithms import find_shortest_path, sort_topologically
from graphlib.algorithms import _DistanceTable
from graphlib.graph import AdjacencySetGraph, GraphType


class TestDistanceTable: # pylint: disable=R0201,C0116
    """Collection of test methods exercising the :class:
    graphlib.algorithms._DistanceTable.
    """

    def test_starting_vertex_has_distance_zero_and_itself_as_predecessor(self):
        distance_table = _DistanceTable('A')

        assert distance_table.get_distance_from_start('A') == 0
        assert distance_table.get_predecessor('A') == 'A'

    def test_in_operator_tests_presence_of_entry_for_the_given_vertex(self):
        distance_table = _DistanceTable('A')
        distance_table.update('B', 'A', 4)
        distance_table.update('C', 'A', 2)

        assert 'A' in distance_table
        assert 'B' in distance_table
        assert 'C' in distance_table
        assert 'X' not in distance_table

    def test_updates_leading_to_shorter_distance_are_accepted(self):
        distance_table = _DistanceTable('A')
        distance_table.update('B', 'A', 4)
        distance_table.update('C', 'A', 2)
        distance_table.update('D', 'C', 8)

        assert distance_table.update('D', 'B', 5) == True
        assert distance_table.get_distance_from_start('D') == 5
        assert distance_table.get_predecessor('D') == 'B'

    def updates_leading_to_longer_distance_are_ignored(self):
        distance_table = _DistanceTable('A')
        distance_table.update('B', 'A', 4)
        distance_table.update('C', 'A', 2)
        distance_table.update('D', 'C', 8)

        assert distance_table.update('D', 'B', 9) == False
        assert distance_table.get_distance_from_start('D') == 8
        assert distance_table.get_predecessor('D') == 'C'
    
    @mark.skip('Test case not implemented yet')
    def test_backtracking_reconstructs_proper_shortest_path(self):
        distance_table = _DistanceTable('A')
        distance_table.update('B', 'A', 2)
        distance_table.update('C', 'A', 3)
        distance_table.update('D', 'C', 6)
        distance_table.update('D', 'B', 4)
        distance_table.update('F', 'B', 4)
        distance_table.update('E', 'D', 9)
        distance_table.update('F', 'E', 12)
        distance_table.update('G', 'F', 15)

        # search_result = distance_table.backtrack_shortest_path('G')
        # assert search_result == ShortestPathSearchResult(tuple(
        #     Edge(start='A', destination='B', weight=2),
        #     Edge(start='B', destination='F', weight=2),
        #     Edge(start='F', destination='G', weight=3),
        # ))

    def test_attempt_to_get_distance_for_non_existent_vertex_leads_to_error(self):
        distance_table = _DistanceTable('A')
        distance_table.update('B', 'A', 4)

        with raises(ValueError, match=r'No distance table entry found for the vertex X\.'):
            distance_table.get_distance_from_start('X')

    def test_attempt_to_get_predecessor_for_non_existent_vertex_leads_to_error(self):
        distance_table = _DistanceTable('A')
        distance_table.update('B', 'A', 4)

        with raises(ValueError, match=r'No distance table entry found for the vertex Y\.'):
            distance_table.get_predecessor('Y')


class TestTopologicalSort: # pylint: disable=R0201,C0116
    """Collection of test methods exercising the :method:
    graphlib.algorithms.sort_toplogically.
    """

    def test_topological_sort_returns_vertices_in_proper_order_case_01(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('C', 'E')
        graph.add_edge('D', 'E')
        graph.add_edge('E', 'F')

        sort_result = sort_topologically(graph)
        actual_order = list(sort_result)
        assert actual_order in [
            ['A', 'B', 'C', 'D', 'E', 'F'],
            ['B', 'A', 'C', 'D', 'E', 'F'],
            ['A', 'B', 'D', 'C', 'E', 'F'],
            ['B', 'A', 'D', 'C', 'E', 'F'],
            ['A', 'D', 'B', 'C', 'E', 'F'],
            ['B', 'D', 'A', 'C', 'E', 'F'],
            ['D', 'A', 'B', 'C', 'E', 'F'],
            ['D', 'B', 'A', 'C', 'E', 'F'],
        ]

    def test_topological_sort_returns_vertices_in_proper_order_case_02(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('B', 'C')
        graph.add_edge('B', 'D')
        graph.add_edge('D', 'E')
        graph.add_edge('C', 'F')
        graph.add_edge('E', 'F')
        graph.add_edge('F', 'G')

        sort_result = sort_topologically(graph)
        sort_result = list(sort_result)
        assert sort_result in [
            ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            ['A', 'B', 'E', 'C', 'D', 'F', 'G'],
            ['A', 'B', 'C', 'E', 'D', 'F', 'G'],
        ]

    def test_topological_sort_returns_vertices_in_proper_order_case_03(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('B', 'C')
        graph.add_edge('C', 'D')
        graph.add_edge('C', 'E')
        graph.add_edge('C', 'F')
        graph.add_edge('D', 'G')
        graph.add_edge('E', 'G')
        graph.add_edge('G', 'H')
        graph.add_edge('F', 'H')
        graph.add_edge('H', 'I')

        sort_result = sort_topologically(graph)
        sort_result = list(sort_result)
        assert sort_result in [
            ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
            ['A', 'B', 'C', 'D', 'F', 'E', 'G', 'H', 'I'],
            ['A', 'B', 'C', 'E', 'D', 'F', 'G', 'H', 'I'],
            ['A', 'B', 'C', 'E', 'F', 'D', 'G', 'H', 'I'],
            ['A', 'B', 'C', 'F', 'E', 'D', 'G', 'H', 'I'],
            ['A', 'B', 'C', 'F', 'D', 'E', 'G', 'H', 'I'],
            ['A', 'B', 'C', 'D', 'E', 'G', 'F', 'H', 'I'],
            ['A', 'B', 'C', 'E', 'D', 'G', 'F', 'H', 'I'],
        ]

    def test_attempt_to_apply_topological_sort_to_undirected_graph_leads_to_exception(self):
        graph = AdjacencySetGraph(GraphType.UNDIRECTED)
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('C', 'D')

        with raises(ValueError, match=r'.+ applied to directed graphs\.'):
            sort_topologically(graph)

    def test_attepmt_to_apply_topological_sort_to_cyclic_graph_leads_to_exception(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('B', 'C')
        graph.add_edge('C', 'A')

        with raises(ValueError, match=r'.+ applied to acyclic graphs\.'):
            sort_topologically(graph)


class TestShortestPath: # pylint: disable=R0201,C0116
    """Collection of test methods exercising the :class:
    graphlib.algorithms.ShortestPathSearchResult.
    """

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

    @mark.skip('Failing - the tested functionality does not seem to work yet')
    def test_shortest_path_search_finds_proper_shortest_path_for_unweighted_graph_case01(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')
        graph.add_edge('A', 'D')
        graph.add_edge('B', 'E')
        graph.add_edge('E', 'F')
        graph.add_edge('C', 'G')
        graph.add_edge('C', 'H')
        graph.add_edge('G', 'E')
        graph.add_edge('F', 'I')
        graph.add_edge('H', 'I')
        graph.add_edge('I', 'L')
        graph.add_edge('L', 'M')
        graph.add_edge('D', 'J')
        graph.add_edge('J', 'K')
        graph.add_edge('K', 'M')

        search_request = ShortestPathSearchRequest(graph, start = 'A', destination = 'L')
        actual_search_result = find_shortest_path(search_request)

        path = [
            Edge(start='A', destination='D', weight=1),
            Edge(start='D', destination='J', weight=1),
            Edge(start='J', destination='K', weight=1),
            Edge(start='K', destination='M', weight=1),
        ]
        expected_search_result = ShortestPathSearchResult(tuple(path))
        assert expected_search_result == actual_search_result

    @mark.skip('Functionality not implemented yet')
    def test_shortest_path_search_finds_proper_shortest_path_for_weighted_graph(self):
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
            Edge(start='A', destination='B', weight=2),
            Edge(start='B', destination='C', weight=1),
            Edge(start='C', destination='F', weight=3),
            Edge(start='F', destination='G', weight=2),
        ]
        expected_search_result = ShortestPathSearchResult(tuple(path))
        assert expected_search_result == actual_search_result
