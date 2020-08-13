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

from pytest import raises

from graphlib.graph import AbstractGraph, AdjacencyMatrixGraph, AdjacencySetGraph, Edge, GraphType

# pylint: disable=R0201,C0116


class AbstractGraphTestFixture(ABC):
    """Abstract test-fixture class that implements test methods common to various
    graph implementations like adjacency matrix or adjacency set.

    This class is supposed to be used as base class for test fixtures for specific
    graph implementations. In concrete terms, a separate subclass per graph
    implementation is the most likely design. The test methods provided by this
    abstract base class use the :method: AbstractGraphTestFixture._create_graph
    to instantiate the proper graph implementation. Derived classes are supposed
    to implement the above mentioned abstract method.
    """

    @abstractmethod
    def _create_graph(self, graph_type: GraphType) -> AbstractGraph:
        """Factory method that is supposed to create the tested graph.

        Args:
            graph_type (GraphType): The graph type to be created
                                    (directed/undirected).

        Raises:
            NotImplementedError: Always as this is just an abstract method.

        Returns:
            AbstractGraph: Derived classes are supposed to return an instance
                           of a concrete subclass of the :class:
                           graphlib.graph.AbstractGraph.
        """
        raise NotImplementedError

    def test_graph_with_all_edges_having_the_same_weight_is_unweighted(self):
        graph = self._create_graph(GraphType.DIRECTED)
        graph.add_edge('A', 'B', 3)
        graph.add_edge('A', 'C', 3)
        graph.add_edge('B', 'C', 3)
        graph.add_edge('C', 'D', 3)

        assert not graph.is_weighted

    def test_graph_with_edges_having_distinct_weights_is_weighted(self):
        graph = self._create_graph(GraphType.DIRECTED)
        graph.add_edge('A', 'B', 2)
        graph.add_edge('A', 'C', 3)
        graph.add_edge('B', 'C', 2)
        graph.add_edge('C', 'D', 4)

        assert graph.is_weighted

    def test_empty_graph_has_no_vertices(self):
        graph = self._create_graph(GraphType.DIRECTED)
        assert graph.vertex_count == 0, 'Vertex count'
        assert graph.get_sorted_vertices() == (), 'Sorted vertices'

    def test_non_empty_graph_returns_proper_number_of_vertices(self):
        graph = self._create_graph(GraphType.DIRECTED)

        graph.add_edge('A', 'B')
        assert graph.vertex_count == 2, 'After A -> B'

        graph.add_edge('A', 'C')
        assert graph.vertex_count == 3, 'After A -> C'

        graph.add_edge('B', 'C')
        assert graph.vertex_count == 3, 'After B -> C'

        graph.add_edge('B', 'E')
        assert graph.vertex_count == 4, 'After B -> E'

        graph.add_edge('C', 'D')
        assert graph.vertex_count == 5, 'After C -> D'

        graph.add_edge('D', 'F')
        assert graph.vertex_count == 6, 'After D -> F'

        graph.add_edge('F', 'E')
        assert graph.vertex_count == 6, 'After F -> E'

    def test_non_empty_graph_returns_proper_list_of_vertices(self):
        graph = self._create_graph(GraphType.DIRECTED)

        graph.add_edge('A', 'B')
        assert graph.get_sorted_vertices() == ('A', 'B'), 'After A -> B'

        graph.add_edge('A', 'C')
        assert graph.get_sorted_vertices() == ('A', 'B', 'C'), 'After A -> C'

        graph.add_edge('B', 'C')
        assert graph.get_sorted_vertices() == ('A', 'B', 'C'), 'After B -> C'

        graph.add_edge('B', 'E')
        assert graph.get_sorted_vertices() == ('A', 'B', 'C', 'E'), 'After B -> E'

        graph.add_edge('C', 'D')
        assert graph.get_sorted_vertices() == ('A', 'B', 'C', 'D', 'E'), 'After C -> D'

        graph.add_edge('D', 'F')
        assert graph.get_sorted_vertices() == ('A', 'B', 'C', 'D', 'E', 'F'), 'After D -> F'

        graph.add_edge('F', 'E')
        assert graph.get_sorted_vertices() == ('A', 'B', 'C', 'D', 'E', 'F'), 'After F -> E'

    def test_proper_in_degree_is_returned(self):
        graph = self._create_graph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('B', 'E')
        graph.add_edge('C', 'D')
        graph.add_edge('D', 'F')
        graph.add_edge('F', 'E')

        assert graph.get_in_degree('A') == 0
        assert graph.get_in_degree('B') == 1
        assert graph.get_in_degree('C') == 2
        assert graph.get_in_degree('D') == 1
        assert graph.get_in_degree('E') == 2
        assert graph.get_in_degree('F') == 1

    def test_proper_edge_weight_is_returned(self):
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

        assert graph.get_edge_weight('A', 'B') == 2, 'A -> B'
        assert graph.get_edge_weight('A', 'C') == 3, 'A -> C'
        assert graph.get_edge_weight('B', 'C') == 5, 'B -> C'
        assert graph.get_edge_weight('B', 'E') == 4, 'B -> E'
        assert graph.get_edge_weight('C', 'D') == 7, 'C -> D'
        assert graph.get_edge_weight('D', 'F') == 3, 'D -> F'
        assert graph.get_edge_weight('F', 'E') == 5, 'F -> E'

    def test_proper_adjacent_vertices_are_returned_for_directed_graph(self):
        # be aware of the fact that this test case also covers vertices that are
        # only the destination of an edge (they are not the start of any edge)
        graph = self._create_graph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('B', 'E')
        graph.add_edge('C', 'D')
        graph.add_edge('D', 'F')
        graph.add_edge('F', 'E')

        assert graph.get_adjacent_vertices('A') == ('B', 'C'), 'A'
        assert graph.get_adjacent_vertices('B') == ('C', 'E'), 'B'
        assert graph.get_adjacent_vertices('C') == ('D', ), 'C'
        assert graph.get_adjacent_vertices('D') == ('F', ), 'D'
        assert graph.get_adjacent_vertices('E') == (), 'E'
        assert graph.get_adjacent_vertices('F') == ('E', ), 'F'

    def test_proper_adjacent_vertices_are_returned_for_undirected_graph(self):
        graph = self._create_graph(GraphType.UNDIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('B', 'E')
        graph.add_edge('C', 'D')
        graph.add_edge('D', 'F')
        graph.add_edge('F', 'E')

        assert graph.get_adjacent_vertices('A') == ('B', 'C'), 'A'
        assert graph.get_adjacent_vertices('B') == ('A', 'C', 'E'), 'B'
        assert graph.get_adjacent_vertices('C') == ('A', 'B', 'D'), 'C'
        assert graph.get_adjacent_vertices('D') == ('C', 'F'), 'D'
        assert graph.get_adjacent_vertices('E') == ('B', 'F'), 'E'
        assert graph.get_adjacent_vertices('F') == ('D', 'E'), 'F'

    def test_get_outgoing_edges_for_existent_vertex_returns_proper_tuple_of_edges(self):
        graph = self._create_graph(GraphType.DIRECTED)
        graph.add_edge('A', 'B', 2)
        graph.add_edge('A', 'C', 3)
        graph.add_edge('B', 'C', 5)
        graph.add_edge('C', 'D', 4)

        assert graph.get_outgoing_edges('D') == ()
        assert graph.get_outgoing_edges('B') == (
            Edge(start='B', destination='C', weight=5),
        )
        assert graph.get_outgoing_edges('A') == (
            Edge(start='A', destination='B', weight=2),
            Edge(start='A', destination='C', weight=3),
        )

    def test_attempt_to_get_outgoing_edges_for_non_existent_vertex_leads_to_error(self):
        graph = self._create_graph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('C', 'D')

        with raises(ValueError, match='Vertex with the name X not found.'):
            graph.get_outgoing_edges('X')

    def test_attempt_to_get_edge_weight_for_non_existent_start_vertex_leads_to_error(self):
        graph = self._create_graph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('C', 'D')

        with raises(ValueError, match='Vertex with the name X not found.'):
            graph.get_edge_weight('X', 'B')

    def test_attempt_to_get_edge_weight_for_non_existent_destination_vertex_leads_to_error(self):
        graph = self._create_graph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('C', 'D')

        with raises(ValueError, match='Vertex with the name X not found.'):
            graph.get_edge_weight('B', 'X')

    def test_attempt_to_get_edge_weight_for_non_existent_edge_leads_to_error(self):
        graph = self._create_graph(GraphType.DIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('C', 'D')

        with raises(ValueError, match='There is no edge from B to A.'):
            graph.get_edge_weight('B', 'A')

    def test_get_all_edges_for_directed_graph_returns_proper_tuple_of_edges(self):
        graph = self._create_graph(GraphType.DIRECTED)
        graph.add_edge('A', 'B', 3)
        graph.add_edge('A', 'C', 2)
        graph.add_edge('B', 'C', 5)
        graph.add_edge('C', 'D', 7)

        all_edges = graph.get_all_edges()

        assert Edge(start='A', destination='B', weight=3) in all_edges
        assert Edge(start='A', destination='C', weight=2) in all_edges
        assert Edge(start='B', destination='C', weight=5) in all_edges
        assert Edge(start='C', destination='D', weight=7) in all_edges

    def test_get_all_edges_for_undirected_graph_returns_proper_tuple_of_edges(self):
        graph = self._create_graph(GraphType.UNDIRECTED)
        graph.add_edge('A', 'B')
        graph.add_edge('A', 'C')
        graph.add_edge('B', 'C')
        graph.add_edge('C', 'D')

        all_edges = graph.get_all_edges()

        for vertex_one, vertex_two in ('A', 'B'), ('A', 'C'), ('B', 'C'), ('C', 'D'):
            assert Edge(start=vertex_one, destination=vertex_two, weight=1) in all_edges
            assert Edge(start=vertex_two, destination=vertex_one, weight=1) in all_edges

    def test_get_all_edges_for_empty_graph_returns_empty_tuple(self):
        graph = self._create_graph(GraphType.UNDIRECTED)

        assert graph.get_all_edges() == tuple()


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
