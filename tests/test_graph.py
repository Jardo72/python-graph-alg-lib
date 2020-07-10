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

"""Unit tests for the graphlib.graph module.
"""

from abc import ABC, abstractmethod

from pytest import mark, raises

from graphlib.graph import AbstractGraph, AdjacencyMatrixGraph, AdjacencySetGraph, GraphType


class AbstractGraphTestFixture(ABC):
    """Abstract test-fixture class that implements test methods common to various
    graph implementations like adjacency matrix or adjacency set.

    This class is supposed to be used as base class for test fixtures for specific
    graph implementations. In concrete terms, a separate subclass per graph
    implementation is the most likely design. The test methods provided by this
    abstract base class use the :method: AbstractGraphTestFixture._create_graph
    to instantiate the proper graph implementation. Derived classes are 
    """

    @abstractmethod
    def _create_graph(self, graph_type: GraphType) -> AbstractGraph:
        """Factory method that is supposed to create the tested graph.

        Args:
            graph_type (GraphType): The graph type to be created
                                    (directed/undirected).

        Raises:
            NotImplementedError: Always as this just an abstract method.

        Returns:
            AbstractGraph: Derived classes are supposed to return an instance
                           of a concrete subclass of the :class:
                           graphlib.graph.AbstractGraph.
        """
        raise NotImplementedError

    def test_empty_graph_has_no_vertices(self): # pylint: disable=R0201
        graph = self._create_graph(GraphType.DIRECTED)
        assert 0 == graph.vertex_count, 'Vertex count'
        assert () == graph.get_sorted_vertices(), 'Sorted vertices'

    def test_non_empty_graph_returns_proper_number_of_vertices(self): # pylint: disable=R0201
        graph = self._create_graph(GraphType.DIRECTED)

        graph.add_edge('A', 'B')
        assert 2 == graph.vertex_count, 'After A -> B'

        graph.add_edge('A', 'C')
        assert 3 == graph.vertex_count, 'After A -> C'

        graph.add_edge('B', 'C')
        assert 3 == graph.vertex_count, 'After B -> C'

        graph.add_edge('B', 'E')
        assert 4 == graph.vertex_count, 'After B -> E'

        graph.add_edge('C', 'D')
        assert 5 == graph.vertex_count, 'After C -> D'

        graph.add_edge('D', 'F')
        assert 6 == graph.vertex_count, 'After D -> F'

        graph.add_edge('F', 'E')
        assert 6 == graph.vertex_count, 'After F -> E'

    def test_non_empty_graph_returns_proper_list_of_vertices(self): # pylint: disable=R0201
        graph = self._create_graph(GraphType.DIRECTED)

        graph.add_edge('A', 'B')
        assert ('A', 'B') == graph.get_sorted_vertices(), 'After A -> B'

        graph.add_edge('A', 'C')
        assert ('A', 'B', 'C') == graph.get_sorted_vertices(), 'After A -> C'

        graph.add_edge('B', 'C')
        assert ('A', 'B', 'C') == graph.get_sorted_vertices(), 'After B -> C'

        graph.add_edge('B', 'E')
        assert ('A', 'B', 'C', 'E') == graph.get_sorted_vertices(), 'After B -> E'

        graph.add_edge('C', 'D')
        assert ('A', 'B', 'C', 'D', 'E') == graph.get_sorted_vertices(), 'After C -> D'

        graph.add_edge('D', 'F')
        assert ('A', 'B', 'C', 'D', 'E', 'F') == graph.get_sorted_vertices(), 'After D -> F'

        graph.add_edge('F', 'E')
        assert ('A', 'B', 'C', 'D', 'E', 'F') == graph.get_sorted_vertices(), 'After F -> E'

    def test_proper_edge_weight_is_returned(self): # pylint: disable=R0201
        # TODO:
        # - for undirected graph, we should test both directions
        # - for directed graph, the opposite direction should lead to error
        # - if weight is not specified, 1 is used as default
        graph = self._create_graph(GraphType.DIRECTED)
        graph.add_edge('A', 'B', 2)
        graph.add_edge('A', 'C', 3)
        graph.add_edge('B', 'C', 5)
        graph.add_edge('B', 'E', 4)
        graph.add_edge('C', 'D', 7)
        graph.add_edge('D', 'F', 3)
        graph.add_edge('F', 'E', 5)

        assert 2 == graph.get_edge_weight('A', 'B'), 'A -> B'
        assert 3 == graph.get_edge_weight('A', 'C'), 'A -> C'
        assert 5 == graph.get_edge_weight('B', 'C'), 'B -> C'
        assert 4 == graph.get_edge_weight('B', 'E'), 'B -> E'
        assert 7 == graph.get_edge_weight('C', 'D'), 'C -> D'
        assert 3 == graph.get_edge_weight('D', 'F'), 'D -> F'
        assert 5 == graph.get_edge_weight('F', 'E'), 'F -> E'

    def test_proper_adjacent_vertices_are_returned_for_directed_graph(self): # pylint: disable=R0201
        graph = self._create_graph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('B', 'E')
        graph.add_edge('C', 'D')
        graph.add_edge('D', 'F')
        graph.add_edge('F', 'E')

        assert ('B', 'C') == graph.get_adjacent_vertices('A'), 'A'
        assert ('C', 'E') == graph.get_adjacent_vertices('B'), 'B'
        assert ('D', ) == graph.get_adjacent_vertices('C'), 'C'
        assert ('F', ) == graph.get_adjacent_vertices('D'), 'D'
        assert () == graph.get_adjacent_vertices('E'), 'E'
        assert ('E', ) == graph.get_adjacent_vertices('F'), 'F'

    def test_proper_adjacent_vertices_are_returned_for_undirected_graph(self): # pylint: disable=R0201
        graph = self._create_graph(GraphType.UNDIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('B', 'E')
        graph.add_edge('C', 'D')
        graph.add_edge('D', 'F')
        graph.add_edge('F', 'E')

        assert ('B', 'C') == graph.get_adjacent_vertices('A'), 'A'
        assert ('A', 'C', 'E') == graph.get_adjacent_vertices('B'), 'B'
        assert ('A', 'B', 'D') == graph.get_adjacent_vertices('C'), 'C'
        assert ('C', 'F') == graph.get_adjacent_vertices('D'), 'D'
        assert ('B', 'F') == graph.get_adjacent_vertices('E'), 'E'
        assert ('D', 'E') == graph.get_adjacent_vertices('F'), 'F'

    def test_attempt_to_get_edge_weight_for_non_existent_start_vertex_leads_to_error(self): # pylint: disable=R0201
        graph = self._create_graph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('C', 'D')

        with raises(ValueError, match=r'Vertex with the name X not found\.'):
            graph.get_edge_weight('X', 'B')

    @mark.skip('Failing - correction is needed in the tested classes')
    def test_attempt_to_get_edge_weight_for_non_existent_destination_vertex_leads_to_error(self): # pylint: disable=R0201
        graph = self._create_graph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('C', 'D')

        with raises(ValueError, match=r'Vertex with the name X not found\.'):
            graph.get_edge_weight('B', 'X')

    def test_attempt_to_get_edge_weight_for_non_existent_edge_leads_to_error(self): # pylint: disable=R0201
        graph = self._create_graph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('C', 'D')

        with raises(ValueError, match=r'There is no edge from B to A\.'):
            graph.get_edge_weight('B', 'A')


class TestAdjacencySetGraph(AbstractGraphTestFixture):
    """Concrete test-fixture for the adjacency set implementation of graph
    (i.e. for the class :class: graph.AdjacencySetGraph).
    """

    def _create_graph(self, graph_type: GraphType) -> AbstractGraph:
        """Creates and returns a new instance of the class :class:
        graph.AdjacencySetGraph, representing the given graph type.
        """
        return AdjacencySetGraph(graph_type)


class TestAdjacencyMatrixGraph(AbstractGraphTestFixture):
    """Concrete test-fixture for the adjacency matric implementation of graph
    (i.e. for the :class: graphlib.graph.AdjacencyMatrixGraph).
    """

    def _create_graph(self, graph_type: GraphType) -> AbstractGraph:
        """Creates and returns a new instance of the class :class:
        graphlib.graph.AdjacencyMatrixGraph, representing the given graph type.
        """
        return AdjacencyMatrixGraph(20, graph_type)
