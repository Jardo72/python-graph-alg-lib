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

from itertools import permutations

from pytest import raises

from graphlib.algorithms import MinimumSpanningTreeAlgorithm, ShortestPathSearchRequest, ShortestPathSearchResult
from graphlib.algorithms import MinimumSpanningTreeSearchRequest, MinimumSpanningTreeSearchResult
from graphlib.algorithms import find_minimum_spanning_tree, find_shortest_path, sort_topologically
from graphlib.algorithms import _DistanceTable
from graphlib.graph import AdjacencySetGraph, Edge, GraphType


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

    def updates_leading_to_equal_distance_are_ignored(self):
        distance_table = _DistanceTable('A')
        distance_table.update('B', 'A', 2)
        distance_table.update('C', 'A', 2)
        distance_table.update('D', 'C', 5)

        assert distance_table.update('D', 'B', 5) == False

    def updates_leading_to_longer_distance_are_ignored(self):
        distance_table = _DistanceTable('A')
        distance_table.update('B', 'A', 4)
        distance_table.update('C', 'A', 2)
        distance_table.update('D', 'C', 8)

        assert distance_table.update('D', 'B', 9) == False
        assert distance_table.get_distance_from_start('D') == 8
        assert distance_table.get_predecessor('D') == 'C'
    
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

        distance_table.backtrack_shortest_path('G') == ShortestPathSearchResult((
            Edge(start='A', destination='B', weight=2),
            Edge(start='B', destination='F', weight=2),
            Edge(start='F', destination='G', weight=3),
        ))

    def test_attempt_to_get_distance_for_non_existent_vertex_leads_to_error(self):
        distance_table = _DistanceTable('A')
        distance_table.update('B', 'A', 4)

        with raises(ValueError, match='No distance table entry found for the vertex X.'):
            distance_table.get_distance_from_start('X')

    def test_attempt_to_get_predecessor_for_non_existent_vertex_leads_to_error(self):
        distance_table = _DistanceTable('A')
        distance_table.update('B', 'A', 4)

        with raises(ValueError, match='No distance table entry found for the vertex Y.'):
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
        sort_result = list(sort_result)

        assert sort_result in [
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
        graph.add_edge('B', 'E')
        graph.add_edge('C', 'F')
        graph.add_edge('D', 'F')
        graph.add_edge('E', 'F')
        graph.add_edge('F', 'G')

        sort_result = sort_topologically(graph)
        sort_result = list(sort_result)

        assert sort_result in [
            ['A', 'B'] + list(p) + ['F', 'G'] for p in permutations('CDE', 3)
        ]

    def test_topological_sort_returns_vertices_in_proper_order_case_03(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('C', 'D')
        graph.add_edge('B', 'E')
        graph.add_edge('D', 'E')
        graph.add_edge('E', 'F')

        sort_result = sort_topologically(graph)
        sort_result = list(sort_result)

        assert sort_result in [
            ['A', 'B', 'C', 'D', 'E', 'F'],
            ['A', 'C', 'B', 'D', 'E', 'F'],
            ['A', 'C', 'D', 'B', 'E', 'F'],
            ['C', 'D', 'A', 'B', 'E', 'F'],
            ['C', 'A', 'D', 'B', 'E', 'F'],
            ['C', 'A', 'B', 'D', 'E', 'F'],
        ]

    def test_topological_sort_returns_vertices_in_proper_order_case_04(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('D', 'F')
        graph.add_edge('E', 'F')
        graph.add_edge('C', 'G')
        graph.add_edge('F', 'G')

        sort_result = sort_topologically(graph)
        sort_result = list(sort_result)

        assert len(sort_result) == 7
        for vertex in 'ABCDEFG':
            assert vertex in sort_result
        assert sort_result.index('A') < sort_result.index('C')
        assert sort_result.index('B') < sort_result.index('C')
        assert sort_result.index('D') < sort_result.index('F')
        assert sort_result.index('E') < sort_result.index('F')
        assert sort_result.index('C') < sort_result.index('G')
        assert sort_result.index('F') < sort_result.index('G')

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


class TestShortestPathSearchResult: # pylint: disable=R0201,C0116
    """Collection of test methods exercising the :class:
    graphlib.algorithms.ShortestPathSearchResult class.
    """

    def test_shortest_path_search_result_provides_proper_derived_properties(self):
        path = (
            Edge(start='A', destination='B', weight=2),
            Edge(start='B', destination='C', weight=3),
            Edge(start='C', destination='F', weight=5),
            Edge(start='F', destination='H', weight=2),
            Edge(start='H', destination='L', weight=7),
        )
        shortest_path = ShortestPathSearchResult(path)

        assert 'A' == shortest_path.start
        assert 'L' == shortest_path.destination
        assert 19 == shortest_path.overall_distance


class TestShortestPathSearchForUnweightedGraphSuiteOne: # pylint: disable=R0201,C0116
    """Collection of test methods exercising the method :method:
    graphlib.algorithms.find_shortest_path for unweighted graphs.
    """

    def _create_tested_graph(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'D')
        graph.add_edge('C', 'D')
        graph.add_edge('D', 'E')
        graph.add_edge('E', 'F')
        graph.add_edge('C', 'E')
        graph.add_edge('B', 'F')
        return graph

    def test_path_from_A_to_F(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='A', destination='F')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='A', destination='B', weight=1),
            Edge(start='B', destination='F', weight=1),
        ))

    def test_path_from_A_to_E(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='A', destination='E')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='A', destination='C', weight=1),
            Edge(start='C', destination='E', weight=1),
        ))


class TestShortestPathSearchForUnweightedGraphSuiteTwo: # pylint: disable=R0201,C0116
    """Collection of test methods exercising the method :method:
    graphlib.algorithms.find_shortest_path for unweighted graphs.
    """

    def _create_tested_graph(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'D')
        graph.add_edge('C', 'D')
        graph.add_edge('C', 'E')
        graph.add_edge('D', 'E')
        graph.add_edge('E', 'F')
        graph.add_edge('F', 'G')
        graph.add_edge('F', 'H')
        graph.add_edge('G', 'H')
        graph.add_edge('H', 'I')
        return graph

    def test_path_from_A_to_I(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='A', destination='I')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='A', destination='C', weight=1),
            Edge(start='C', destination='E', weight=1),
            Edge(start='E', destination='F', weight=1),
            Edge(start='F', destination='H', weight=1),
            Edge(start='H', destination='I', weight=1),
        ))

    def test_path_from_B_to_G(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='B', destination='G')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='B', destination='D', weight=1),
            Edge(start='D', destination='E', weight=1),
            Edge(start='E', destination='F', weight=1),
            Edge(start='F', destination='G', weight=1),
        ))


class TestShortestPathSearchForUnweightedGraphSuiteThree: # pylint: disable=R0201,C0116
    """Collection of test methods exercising the method :method:
    graphlib.algorithms.find_shortest_path for unweighted graphs.
    """

    def _create_tested_graph(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('B', 'C')
        graph.add_edge('C', 'B')
        graph.add_edge('C', 'D')
        graph.add_edge('A', 'E')
        graph.add_edge('B', 'F')
        graph.add_edge('F', 'A')
        graph.add_edge('C', 'G')
        graph.add_edge('H', 'D')
        graph.add_edge('F', 'E')
        graph.add_edge('F', 'G')
        graph.add_edge('G', 'F')
        graph.add_edge('H', 'G')
        graph.add_edge('E', 'I')
        graph.add_edge('J', 'F')
        graph.add_edge('F', 'K')
        graph.add_edge('K', 'H')
        graph.add_edge('L', 'H')
        graph.add_edge('J', 'I')
        graph.add_edge('K', 'J')
        graph.add_edge('L', 'K')
        graph.add_edge('M', 'I')
        graph.add_edge('J', 'N')
        graph.add_edge('P', 'J')
        graph.add_edge('P', 'L')
        graph.add_edge('N', 'M')
        graph.add_edge('N', 'O')
        graph.add_edge('O', 'P')
        graph.add_edge('P', 'O')
        return graph

    def test_path_from_A_to_D(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='A', destination='D')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='A', destination='B', weight=1),
            Edge(start='B', destination='C', weight=1),
            Edge(start='C', destination='D', weight=1),
        ))

    def test_path_from_A_to_I(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='A', destination='I')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='A', destination='E', weight=1),
            Edge(start='E', destination='I', weight=1),
        ))

    def test_path_from_A_to_M(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='A', destination='M')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='A', destination='B', weight=1),
            Edge(start='B', destination='F', weight=1),
            Edge(start='F', destination='K', weight=1),
            Edge(start='K', destination='J', weight=1),
            Edge(start='J', destination='N', weight=1),
            Edge(start='N', destination='M', weight=1),
        ))

    def test_path_from_A_to_P(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='A', destination='P')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='A', destination='B', weight=1),
            Edge(start='B', destination='F', weight=1),
            Edge(start='F', destination='K', weight=1),
            Edge(start='K', destination='J', weight=1),
            Edge(start='J', destination='N', weight=1),
            Edge(start='N', destination='O', weight=1),
            Edge(start='O', destination='P', weight=1),
        ))

    def test_path_from_P_to_A(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='P', destination='A')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='P', destination='J', weight=1),
            Edge(start='J', destination='F', weight=1),
            Edge(start='F', destination='A', weight=1),
        ))

    def test_path_from_P_to_C(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='P', destination='C')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='P', destination='J', weight=1),
            Edge(start='J', destination='F', weight=1),
            Edge(start='F', destination='A', weight=1),
            Edge(start='A', destination='B', weight=1),
            Edge(start='B', destination='C', weight=1),
        ))

    def test_path_from_P_to_G(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='P', destination='G')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='P', destination='J', weight=1),
            Edge(start='J', destination='F', weight=1),
            Edge(start='F', destination='G', weight=1),
        ))

    def test_path_from_P_to_M(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='P', destination='M')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='P', destination='J', weight=1),
            Edge(start='J', destination='N', weight=1),
            Edge(start='N', destination='M', weight=1),
        ))


class TestShortestPathSearchForWeightedGraphSuiteOne: # pylint: disable=R0201,C0116
    """Collection of test methods exercising the method :method:
    graphlib.algorithms.find_shortest_path for weighted graphs.
    """

    def _create_tested_graph(self):
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
        return graph

    def test_path_from_A_to_G(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start = 'A', destination = 'G')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='A', destination='B', weight=2),
            Edge(start='B', destination='C', weight=1),
            Edge(start='C', destination='F', weight=3),
            Edge(start='F', destination='G', weight=2),
        ))

    def test_path_from_B_to_G(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='B', destination='G')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='B', destination='C', weight=1),
            Edge(start='C', destination='F', weight=3),
            Edge(start='F', destination='G', weight=2),
        ))

    def test_path_from_D_to_G(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='D', destination='G')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='D', destination='C', weight=3),
            Edge(start='C', destination='F', weight=3),
            Edge(start='F', destination='G', weight=2),
        ))

    def test_path_from_A_to_E(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='A', destination='E')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='A', destination='B', weight=2),
            Edge(start='B', destination='E', weight=5),
        ))

    def test_path_from_D_to_E(self):
        graph = self._create_tested_graph()

        search_request = ShortestPathSearchRequest(graph, start='D', destination='E')
        assert find_shortest_path(search_request) == ShortestPathSearchResult((
            Edge(start='D', destination='C', weight=3),
            Edge(start='C', destination='F', weight=3),
            Edge(start='F', destination='E', weight=5),
        ))


class TestShortestPathSearchForWeightedGraphSuiteTwo: # pylint: disable=R0201,C0116
    """Collection of test methods exercising the method :method:
    graphlib.algorithms.find_shortest_path for weighted graphs.
    """

    def _create_tested_graph(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'D', 3)
        graph.add_edge('B', 'D', 2)
        graph.add_edge('D', 'C', 2)
        graph.add_edge('C', 'E', 2)
        graph.add_edge('D', 'F', 8)
        graph.add_edge('D', 'G', 6)
        graph.add_edge('E', 'F', 1)
        graph.add_edge('E', 'H', 4)
        graph.add_edge('F', 'H', 2)
        graph.add_edge('F', 'G', 3)
        graph.add_edge('H', 'G', 4)
        return graph

    def test_path_from_A_to_G(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='A', destination='G')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='A', destination='D', weight=3),
            Edge(start='D', destination='G', weight=6),
        ))

    def test_path_from_A_to_H(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='A', destination='H')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='A', destination='D', weight=3),
            Edge(start='D', destination='C', weight=2),
            Edge(start='C', destination='E', weight=2),
            Edge(start='E', destination='F', weight=1),
            Edge(start='F', destination='H', weight=2),
        ))

    def test_path_from_C_to_G(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='C', destination='G')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='C', destination='E', weight=2),
            Edge(start='E', destination='F', weight=1),
            Edge(start='F', destination='G', weight=3),
        ))


class TestShortestPathSearchForWeightedGraphSuiteThree: # pylint: disable=R0201,C0116
    """Collection of test methods exercising the method :method:
    graphlib.algorithms.find_shortest_path for weighted graphs.
    """

    def _create_tested_graph(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'C', 14)
        graph.add_edge('A', 'D', 3)
        graph.add_edge('B', 'D', 5)
        graph.add_edge('B', 'E', 15)
        graph.add_edge('C', 'F', 4)
        graph.add_edge('G', 'C', 5)
        graph.add_edge('D', 'G', 4)
        graph.add_edge('D', 'H', 4)
        graph.add_edge('H', 'E', 3)
        graph.add_edge('E', 'I', 2)
        graph.add_edge('F', 'J', 7)
        graph.add_edge('G', 'J', 32)
        graph.add_edge('G', 'K', 16)
        graph.add_edge('K', 'H', 22)
        graph.add_edge('H', 'L', 16)
        graph.add_edge('I', 'L', 3)
        graph.add_edge('J', 'M', 24)
        graph.add_edge('J', 'N', 6)
        graph.add_edge('K', 'N', 9)
        graph.add_edge('K', 'O', 4)
        graph.add_edge('L', 'O', 18)
        graph.add_edge('L', 'P', 2)
        graph.add_edge('Q', 'M', 5)
        graph.add_edge('N', 'Q', 4)
        graph.add_edge('R', 'N', 6)
        graph.add_edge('O', 'R', 5)
        graph.add_edge('S', 'O', 4)
        graph.add_edge('P', 'S', 6)
        graph.add_edge('Q', 'T', 7)
        graph.add_edge('R', 'T', 28)
        graph.add_edge('R', 'U', 3)
        graph.add_edge('S', 'U', 17)
        return graph

    def test_path_from_A_to_J(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='A', destination='J')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='A', destination='D', weight=3),
            Edge(start='D', destination='G', weight=4),
            Edge(start='G', destination='C', weight=5),
            Edge(start='C', destination='F', weight=4),
            Edge(start='F', destination='J', weight=7),
        ))

    def test_path_from_B_to_I(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='B', destination='I')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='B', destination='D', weight=5),
            Edge(start='D', destination='H', weight=4),
            Edge(start='H', destination='E', weight=3),
            Edge(start='E', destination='I', weight=2),
        ))

    def test_path_from_B_to_M(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='B', destination='M')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='B', destination='D', weight=5),
            Edge(start='D', destination='G', weight=4),
            Edge(start='G', destination='C', weight=5),
            Edge(start='C', destination='F', weight=4),
            Edge(start='F', destination='J', weight=7),
            Edge(start='J', destination='N', weight=6),
            Edge(start='N', destination='Q', weight=4),
            Edge(start='Q', destination='M', weight=5),
        ))

    def test_path_from_K_to_L(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='K', destination='L')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='K', destination='H', weight=22),
            Edge(start='H', destination='E', weight=3),
            Edge(start='E', destination='I', weight=2),
            Edge(start='I', destination='L', weight=3),
        ))

    def test_path_from_L_to_M(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='L', destination='M')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='L', destination='P', weight=2),
            Edge(start='P', destination='S', weight=6),
            Edge(start='S', destination='O', weight=4),
            Edge(start='O', destination='R', weight=5),
            Edge(start='R', destination='N', weight=6),
            Edge(start='N', destination='Q', weight=4),
            Edge(start='Q', destination='M', weight=5),
        ))


class TestShortestPathSearchForWeightedGraphSuiteFour: # pylint: disable=R0201,C0116
    """Collection of test methods exercising the method :method:
    graphlib.algorithms.find_shortest_path for weighted graphs.
    """

    def _create_tested_graph(self):
        graph = AdjacencySetGraph(GraphType.DIRECTED)
        graph.add_edge('A', 'B', 2)
        graph.add_edge('C', 'B', 3)
        graph.add_edge('A', 'D', 8)
        graph.add_edge('B', 'E', 3)
        graph.add_edge('C', 'F', 4)
        graph.add_edge('E', 'D', 2)
        graph.add_edge('F', 'E', 5)
        graph.add_edge('D', 'G', 2)
        graph.add_edge('E', 'H', 10)
        graph.add_edge('I', 'F', 3)
        graph.add_edge('G', 'H', 4)
        graph.add_edge('H', 'I', 2)
        graph.add_edge('J', 'G', 2)
        graph.add_edge('H', 'K', 3)
        graph.add_edge('I', 'L', 12)
        graph.add_edge('K', 'J', 2)
        graph.add_edge('K', 'L', 3)
        return graph

    def test_path_from_A_to_J(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='A', destination='J')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='A', destination='B', weight=2),
            Edge(start='B', destination='E', weight=3),
            Edge(start='E', destination='D', weight=2),
            Edge(start='D', destination='G', weight=2),
            Edge(start='G', destination='H', weight=4),
            Edge(start='H', destination='K', weight=3),
            Edge(start='K', destination='J', weight=2),
        ))

    def test_path_from_F_to_I(self):
        graph = self._create_tested_graph()

        request = ShortestPathSearchRequest(graph, start='F', destination='I')
        assert find_shortest_path(request) == ShortestPathSearchResult((
            Edge(start='F', destination='E', weight=5),
            Edge(start='E', destination='D', weight=2),
            Edge(start='D', destination='G', weight=2),
            Edge(start='G', destination='H', weight=4),
            Edge(start='H', destination='I', weight=2),
        ))


class TestMinimumSpanningTreeSearchResult: # pylint: disable=R0201,C0116
    """Collection of test methods exercising the :class:
    graphlib.algorithms.MinimumSpanningTree class.
    """

    def _create_minimum_spanning_tree(self):
        edges = (
            Edge(start='A', destination='B', weight=2),
            Edge(start='B', destination='C', weight=3),
            Edge(start='C', destination='F', weight=5),
            Edge(start='D', destination='D', weight=2),
        )
        return MinimumSpanningTreeSearchResult(MinimumSpanningTreeAlgorithm.PRIM, 'A', edges)

    def test_overall_weight_is_calculated_properly(self):
        minimum_spanning_tree = self._create_minimum_spanning_tree()

        assert minimum_spanning_tree.overall_weight == 12

    def test_len_function_provides_number_of_edges(self):
        minimum_spanning_tree = self._create_minimum_spanning_tree()

        assert len(minimum_spanning_tree) == 4

    def test_in_operator_verifies_presence_of_edge(self):
        minimum_spanning_tree = self._create_minimum_spanning_tree()

        assert Edge(start='A', destination='B', weight=2) in minimum_spanning_tree
        assert Edge(start='B', destination='C', weight=3) in minimum_spanning_tree

        assert Edge(start='A', destination='B', weight=3) not in minimum_spanning_tree
        assert Edge(start='A', destination='X', weight=2) not in minimum_spanning_tree
        assert Edge(start='X', destination='B', weight=2) not in minimum_spanning_tree


class TestMinimumSpanningTreeSearch: # pylint: disable=R0201,C0116
    """Collection of test methods exercising the :method:
    method graphlib.algorithms.find_minimum_spanning_tree.
    """

    def test_prims_algorithm_01(self):
        graph = AdjacencySetGraph(GraphType.UNDIRECTED)
        graph.add_edge('A', 'B', 5)
        graph.add_edge('A', 'C', 7)
        graph.add_edge('B', 'C', 2)
        graph.add_edge('B', 'D', 3)
        graph.add_edge('B', 'E', 4)
        graph.add_edge('C', 'D', 4)
        graph.add_edge('C', 'E', 6)
        graph.add_edge('D', 'E', 8)
        graph.add_edge('D', 'F', 10)
        graph.add_edge('E', 'F', 4)

        search_request = MinimumSpanningTreeSearchRequest(graph, MinimumSpanningTreeAlgorithm.PRIM, 'A')
        search_result = find_minimum_spanning_tree(search_request)

        assert search_result.overall_weight == 18
        assert len(search_result) == 5
        assert Edge(start='A', destination='B', weight=5) in search_result
        assert Edge(start='B', destination='C', weight=2) in search_result
        assert Edge(start='B', destination='D', weight=3) in search_result
        assert Edge(start='B', destination='E', weight=4) in search_result
        assert Edge(start='E', destination='F', weight=4) in search_result

    def test_prims_algorithm_02(self):
        graph = AdjacencySetGraph(GraphType.UNDIRECTED)
        graph.add_edge('A', 'B', 7)
        graph.add_edge('A', 'C', 8)
        graph.add_edge('A', 'D', 3)
        graph.add_edge('B', 'C', 5)
        graph.add_edge('B', 'E', 2)
        graph.add_edge('C', 'D', 1)
        graph.add_edge('C', 'F', 2)
        graph.add_edge('D', 'G', 6)
        graph.add_edge('E', 'F', 1)
        graph.add_edge('E', 'H', 3)
        graph.add_edge('F', 'G', 2)
        graph.add_edge('F', 'H', 8)
        graph.add_edge('G', 'H', 9)

        search_request = MinimumSpanningTreeSearchRequest(graph, MinimumSpanningTreeAlgorithm.PRIM, 'A')
        search_result = find_minimum_spanning_tree(search_request)

        assert search_result.overall_weight == 14
        assert len(search_result) == 7
        assert Edge(start='A', destination='D', weight=3) in search_result
        assert Edge(start='D', destination='C', weight=1) in search_result
        assert Edge(start='C', destination='F', weight=2) in search_result
        assert Edge(start='F', destination='E', weight=1) in search_result
        assert Edge(start='E', destination='B', weight=2) in search_result
        assert Edge(start='F', destination='G', weight=2) in search_result
        assert Edge(start='E', destination='H', weight=3) in search_result

    def test_prims_algorithm_03(self):
        graph = AdjacencySetGraph(GraphType.UNDIRECTED)
        graph.add_edge('A', 'B', 7)
        graph.add_edge('B', 'C', 4)
        graph.add_edge('A', 'D', 2)
        graph.add_edge('B', 'E', 6)
        graph.add_edge('C', 'F', 1)
        graph.add_edge('D', 'E', 3)
        graph.add_edge('E', 'F', 5)
        graph.add_edge('D', 'G', 5)
        graph.add_edge('E', 'H', 2)
        graph.add_edge('F', 'I', 2)
        graph.add_edge('G', 'H', 2)
        graph.add_edge('H', 'I', 3)
        graph.add_edge('G', 'J', 1)
        graph.add_edge('H', 'K', 7)
        graph.add_edge('I', 'L', 3)
        graph.add_edge('J', 'K', 2)
        graph.add_edge('K', 'L', 8)

        search_request = MinimumSpanningTreeSearchRequest(graph, MinimumSpanningTreeAlgorithm.PRIM, 'A')
        search_result = find_minimum_spanning_tree(search_request)

        assert search_result.overall_weight == 25
        assert len(search_result) == 11
        assert Edge(start='A', destination='D', weight=2) in search_result
        assert Edge(start='D', destination='E', weight=3) in search_result
        assert Edge(start='E', destination='H', weight=2) in search_result
        assert Edge(start='H', destination='G', weight=2) in search_result
        assert Edge(start='G', destination='J', weight=1) in search_result
        assert Edge(start='H', destination='I', weight=3) in search_result
        assert Edge(start='I', destination='L', weight=3) in search_result
        assert Edge(start='I', destination='F', weight=2) in search_result
        assert Edge(start='F', destination='C', weight=1) in search_result
        assert Edge(start='C', destination='B', weight=4) in search_result
        assert Edge(start='J', destination='K', weight=2) in search_result
