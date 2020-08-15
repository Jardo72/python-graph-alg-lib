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

"""This module provides two graph implementations (adjacency matrix,
adjacency set), plus an abstract base class defining the public API of
a graph implementation. The module also involves some internal classes
supporting the above mentioned two graph implementations.
"""

from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from enum import Enum, unique
from typing import Dict, List, Set, Tuple


def _create_matrix(size: int, default_value: int = 0) -> List[List[int]]:
    return [[default_value for _ in range(0, size)] for _ in range(0, size)]


@unique
class GraphType(Enum):
    """Enumeration defining graph types (directed/undirected).
    """

    DIRECTED = 1

    UNDIRECTED = 2


@dataclass(frozen=True)
class Edge:
    """Immutable structure representing a single edge of a graph.
    """
    start: str
    destination: str
    weight: int


class _VertexRegistry:
    """Collection of vertices supporting implementation of graph
    representations.
    """

    def __init__(self):
        """Constructs a new empty vertex registry instance.
        """
        self._sequence: int = 0
        self._name_to_id_mapping = {}
        self._id_to_name_mapping = {}

    def get_id(self, name: str, generate_if_unknown: bool = False) -> int:
        """Returns the unique ID of the vertex with the given name.

        Args:
            name (str): The name of the vertex whose ID is to be returned.
            generate_if_unknown (bool, optional): True if new ID is to be
                                                  generated if no ID has been
                                                  generated for the given vertex
                                                  yet; False (default) if ValueError
                                                  is to be raised if there is ID for
                                                  the given vertex.

        Raises:
            ValueError: If this registry does not contain ID for the given
                        vertex name, and generation of new ID is not requested.

        Returns:
            int: The unique ID of the vertex with the given name.
        """
        if generate_if_unknown and name not in self._name_to_id_mapping:
            new_id = self._generate_new_id()
            self._name_to_id_mapping[name] = new_id
            self._id_to_name_mapping[new_id] = name
        if name not in self._name_to_id_mapping:
            message = f'Vertex with the name {name} not found.'
            raise ValueError(message)
        return self._name_to_id_mapping[name]

    def get_name(self, vertex_id: int) -> str:
        """Returns the name of the vertex with the given vertex ID.

        Args:
            vertex_id (int): Unique ID of the vertex whose name is to be
                             returned.

        Raises:
            ValueError: If this vertex registry does not contain any vertex
                        with the given ID.

        Returns:
            str: The name of the given vertex.
        """
        if not vertex_id in self._id_to_name_mapping:
            message = 'Vertex with the ID {vertex_id} not present in the registry.'
            raise ValueError(message)
        return self._id_to_name_mapping[vertex_id]

    def get_names(self) -> Tuple[str, ...]:
        """Creates and returns a new tuple containing names of all vertices
        contained in this vertex registry.

        Returns:
            Tuple[str, ...]: The cretated tuple with sorted names (ascending
                             order) of all vetices contained in this vertex
                             registry. An empty tuple is returned if this
                             vertex registry is empty.
        """
        return tuple(self._name_to_id_mapping)

    def _generate_new_id(self) -> int:
        """Internal helper method that generates and returns a new unique
        vertex IDs.

        Returns:
            int: The generated new vertex ID.
        """
        result = self._sequence
        self._sequence = self._sequence + 1
        return result

    def __len__(self) -> int:
        """Returns the number of vertices currently contained in the vertex
        registry.

        Returns:
            int: [description]
        """
        return len(self._name_to_id_mapping)


class AbstractGraph(ABC):
    """Abstract base class that prescribes the public API for a graph
    implementation and provides the functionality common to various graph
    implementations.
    """

    def __init__(self, graph_type: GraphType):
        self._graph_type = graph_type

    @property
    def graph_type(self) -> GraphType:
        """Returns the type of the graph represented by this object.

        Returns:
            GrapthType: The graph type of this graph.
        """
        return self._graph_type

    @abstractproperty
    def is_weighted(self) -> bool:
        """Verifies whether this graph is weighted or unweighted.

        A graph is considered as unweighted if all edges it involves have the
        same weight. If a graph involves at at least two edges with distinct
        weight, it is considered as weighted.

        Raises:
            NotImplementedError: This method always raises this exception as
                                 this is an abstract method derived classes
                                 have to implement/override.

        Returns:
            bool: Derived classes implementing this method are supposed to
                  return True if this graph is weighted, and False if this
                  graph is unweighted.
        """
        raise NotImplementedError

    @abstractproperty
    def vertex_count(self) -> int:
        """Returns the number of vertices involved in the graph represented
        byt this object.

        Raises:
            NotImplementedError: This method always raises this exception as
                                 this is an abstract method derived classes
                                 have to implement.

        Returns:
            int: Derived classes implementing this method are supposed to
                 return the number of vertices involved in the graph
                 represented by this object.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_vertices(self, sort: bool = False) -> Tuple[str, ...]:
        """Creates and returns a new tuple containing names of all
        vertices involved in the graph represented by this object.

        If requested, the names are alphabetically sorted in ascending order.

        Args:
            sort (bool): True if the names of the vertices are to be sorted;
                         False otherwise.

        Raises:
            NotImplementedError: This method always raises this exception as
                                 this is an abstract method derived classes
                                 have to implement.

        Returns:
            Tuple[str, ...]: Derived classes implementing this method are
                             supposed to return a new tuple containing the
                             names of all vertices involved in the graph
                             represented by this object in ascending
                             alphabetical order.
        """
        raise NotImplementedError

    @abstractmethod
    def get_adjacent_vertices(self, vertex: str) -> Tuple[str, ...]:
        """Creates and returns a new tuple containing the names of vertices
        adjacent to the vertex with the given name.

        Args:
            vertex (str): The name of the vertex whose adjacent vertices are
            to be returned.

        Raises:
            NotImplementedError: This method always raises this exception as
                                 this is an abstract method derived classes
                                 have to implement.
        Returns:
            Tuple[str, ...]: Derived classes implementing this method are
                             supposed to return a new tuple containing the
                             names of vertices adjacent to the given vertex.
        """
        raise NotImplementedError

    def get_outgoing_edges(self, vertex: str) -> Tuple[Edge, ...]:
        """ Creates and returns a new tuple containing all edges outgoing from the
        given vertex.

        This is a fully functional implementation of this method which is not
        supposed to be overridden by subclasses of this class.

        Args:
            vertex (str): The start vertex of the desired edges.

        Raises:
            ValueError: If this graph does not involve a vertex with the given
                        name.

        Returns:
            Tuple[Edge, ...]: New tuple containing the edges outgoing from the
                              given vertex.
        """
        result = []
        for adjacent_vertex in self.get_adjacent_vertices(vertex):
            weight = self.get_edge_weight(vertex, adjacent_vertex)
            result.append(Edge(vertex, adjacent_vertex, weight))
        return tuple(result)

    def get_all_edges(self) -> Tuple[Edge, ...]:
        """Creates and returns a new tuple containing all edges involved in the graph
        represented by this object.

        If this is an undirected graph, the connection between two connected vertices
        is represented by two edges - one for each direction.

        Returns:
            Tuple[Edge, ...]: New tuple containing all edges involved in the graph
                              represented by this object.
        """
        result = set()
        for vertex in self.get_all_vertices():
            for edge in self.get_outgoing_edges(vertex):
                result.add(edge)
        return tuple(result)

    @abstractmethod
    def add_edge(self, vertex_one: str, vertex_two: str, weight: int = 1):
        """Adds an edge connecting the given pair of vertices to this graph. If
        this graph is a directed graph, an edge from vertex one to vertex two
        is added to this graph. If this graph is undirected, bidirectional
        connectivity is established.

        Args:
            vertex_one (str): Vertex one (source vertex in case of directed
                              graph).
            vertex_two (str): Vertex two (destination vertex in case of
                              directed graph).
            weight (int): The weight of the new edge. If this graph is
                          undirected, the wieght is applied to both
                          directions. This argument is optional - derived
                          classes are supposed to use the value 1 as default.

        Raises:
            NotImplementedError: This method always raises this exception as
                                 this is an abstract method derived classes
                                 have to implement.
        """
        raise NotImplementedError

    @abstractmethod
    def get_edge_weight(self, vertex_one: str, vertex_two: str) -> int:
        """Returns the weight of the edge connecting the given pair of
        vertices.

        Args:
            vertex_one (str): The source vertex of the edge whose weight is
                              to be returned.
            vertex_two (str): The destination vertex of the edge whose weight
                              is to be returned.

        Raises:
            NotImplementedError: This method always raises this exception as
                                 this is an abstract method derived classes
                                 have to implement.

        Returns:
            int: Derived classes implementing this method are supposed to
                 return the weight of the edge connecting the given pair of
                 vertices.
        """
        raise NotImplementedError

    @abstractmethod
    def get_in_degree(self, vertex: str) -> int:
        """Returns the in-degree of the vertex with the given name.

        Args:
            vertex (str): The name of the vertex whose in-degree is to be
                          returned.

        Raises:
            NotImplementedError: This method always raises this exception as
                                 this is an abstract method derived classes
                                 have to implement.

        Returns:
            int: Derived classes implementing this method are supposed to
                 return the number of edges incident to the vertex with the
                 given name.
        """
        raise NotImplementedError


class AdjacencyMatrixGraph(AbstractGraph):
    """Graph implementation based on adjacency matrix.
    """

    def __init__(self, vertex_count: int, graph_type: GraphType):
        """Creates a new adjacency matrix graph of the given type, with
        adjacency matrix for the given number of vertices.

        Args:
            vertex_count (int): The size of the adjacency matrix to be
                                created. This is the maximal number of
                                vertices the created graph can involve.
            graph_type (GraphType): The type of the created graph.
        """
        super().__init__(graph_type)
        self._matrix = _create_matrix(vertex_count)
        self._registry = _VertexRegistry()
        self._weights: Set[int] = set()

    @property
    def is_weighted(self) -> bool:
        """Verifies whether this graph is weighted or unweighted.

        Returns:
            bool: True if this graph is weighted; False if this graph is
                  unweighted.
        """
        return len(self._weights) > 1

    @property
    def vertex_count(self) -> int:
        """Returns the number of vertices involved in the graph represented
        by this object.

        Returns:
            int: The number of vertices involved in the graph represented by
                 this object.
        """
        return len(self._registry)

    def add_edge(self, vertex_one: str, vertex_two: str, weight: int = 1):
        """Adds an edge connecting the given pair of vertices to this graph. If
        this graph is a directed graph, an edge from vertex one to vertex two
        is added to this graph. If this graph is undirected, bidirectional
        connectivity is established.

        Args:
            vertex_one (str): Vertex one (source vertex in case of directed
                              graph).
            vertex_two (str): Vertex two (destination vertex in case of
                              directed graph).
            weight (int): The weight of the new edge. If this graph is
                          undirected, the wieght is applied to both
                          directions. This argument is optional - the
                          value 1 is used as default.
        """
        vertex_one_index = self._registry.get_id(vertex_one, True)
        vertex_two_index = self._registry.get_id(vertex_two, True)
        self._matrix[vertex_one_index][vertex_two_index] = weight
        if self.graph_type is GraphType.UNDIRECTED:
            self._matrix[vertex_two_index][vertex_one_index] = weight
        self._weights.add(weight)

    def get_all_vertices(self, sort: bool = False) -> Tuple[str, ...]:
        """Creates and returns a new tuple containing names of all
        vertices involved in the graph represented by this object.

        Returns:
            Tuple[str, ...]: New tuple containing the names of all vertices
                             involved in the graph represented by this object.
                             If requested, the names are sorted in ascending
                             alphabetical order.
        """
        return tuple(sorted(self._registry.get_names()) if sort else self._registry.get_names())

    def get_adjacent_vertices(self, vertex: str) -> Tuple[str, ...]:
        """Creates and returns a new tuple containing the names of vertices
        adjacent to the vertex with the given name.

        Args:
            vertex (str): The name of the vertex whose adjacent vertices are
            to be returned.

        Returns:
            Tuple[str, ...]: New tuple containing the names of vertices
                             adjacent to the given vertex.
        """
        vertex_index = self._registry.get_id(vertex)
        result = []
        for index, weight in enumerate(self._matrix[vertex_index]):
            if weight > 0:
                name = self._registry.get_name(index)
                result.append(name)
        return tuple(sorted(result))

    def get_edge_weight(self, vertex_one, vertex_two) -> int:
        """Returns the weight of the edge connecting the given pair of
        vertices.

        Args:
            vertex_one (str): The source vertex of the edge whose weight is
                              to be returned.
            vertex_two (str): The destination vertex of the edge whose weight
                              is to be returned.

        Returns:
            int: The weight of the edge connecting the given pair of vertices.
        """
        vertex_one_index = self._registry.get_id(vertex_one)
        vertex_two_index = self._registry.get_id(vertex_two)
        result = self._matrix[vertex_one_index][vertex_two_index]
        if result == 0:
            message = f'There is no edge from {vertex_one} to {vertex_two}.'
            raise ValueError(message)
        return result

    def get_in_degree(self, vertex: str) -> int:
        """Returns the in-degree of the vertex with the given name.

        Args:
            vertex (str): The name of the vertex whose in-degree is to be
                          returned.

        Returns:
            int: The number of edges incident to the vertex with the given
                 name.
        """
        vertex_index = self._registry.get_id(vertex)
        result = 0
        for row in self._matrix:
            if row[vertex_index] > 0:
                result = result + 1
        return result


class _AdjacencySet:
    """Adjacency set storing information about vertices adjacent to a single
    vertex. Instances of this class are to be used by an adjacency set
    implementation of a graph.
    """

    def __init__(self, name: str):
        """Constructs a new adjacency set that is to be used for the vertex
        with the given name.

        Args:
            name (str): The name of the vertex for which the constructed
                        adjacency set is to be used.
        """
        self._name: str = name
        self._adjacent_vertices: Dict[str, int] = {}

    @property
    def name(self) -> str:
        """Returns the name of the vertex whose adjacent vertices are stored
        in this adjacency set.

        Returns:
            str: The name of the vertex corresponding to this adjacency set.
        """
        return self._name

    def add_edge(self, destination: str, weight: int):
        """Adds a new edge to this registry. The new edge connects the vertex
        corresponding to this vertex registry with the given destination
        vertex.

        Args:
            destination (str): The destination vertex of the edge to be added.
            weight (int): [description]
        """
        self._adjacent_vertices[destination] = weight

    def get_adjacent_vertices(self) -> Tuple[str, ...]:
        """Creates and returns a new tuple containing the names of all vertices
        adjacent to the vertex corresponding to this adjacency set.

        Returns:
            Tuple[str, ...]: The created tuple containing the names of adjacent
            vertices in ascending alphabetical order.
        """
        return tuple(sorted(self._adjacent_vertices))

    def get_edge_weight(self, destination: str) -> int:
        """Returns the weight of the edge from the vertex corresponding to
        this adjacency set to the vertex with the given name.

        Args:
            destination (str): The name of the destination vertex.

        Raises:
            ValueError: If this adjacency set contains no destination vertex
                        with the given name.

        Returns:
            int: [description]
        """
        if destination not in self._adjacent_vertices:
            message = f'There is no edge from {self._name} to {destination}.'
            raise ValueError(message)
        return self._adjacent_vertices[destination]

    def __contains__(self, vertex: str) -> bool:
        """Verifies whether a vertex with the given name is currently present
        in this adjacency set.

        Args:
            vertex (str): The vertex name to be verified.

        Returns:
            bool: True if the vertex with the given name is adjacent to the
                  vertex corresponding to this adjacency set; False otherwise.
        """
        return vertex in self._adjacent_vertices


class AdjacencySetGraph(AbstractGraph):
    """Graph implementation based on adjacency set.

    Args:
        _AbstractGraph ([type]): [description]
    """

    def __init__(self, graph_type: GraphType):
        super().__init__(graph_type)
        self._adjacency_sets: Dict[str, _AdjacencySet] = {}
        self._weights: Set[int] = set()

    @property
    def is_weighted(self) -> bool:
        """Verifies whether this graph is weighted or unweighted.

        Returns:
            bool: True if this graph is weighted; False if this graph is
                  unweighted.
        """
        return len(self._weights) > 1

    @property
    def vertex_count(self) -> int:
        """Returns the number of vertices involved in the graph represented
        by this object.

        Returns:
            int: The number of vertices involved in the graph represented by
                 this object.
        """
        return len(self._adjacency_sets)

    def add_edge(self, vertex_one: str, vertex_two: str, weight: int = 1):
        """Adds an edge connecting the given pair of vertices to this graph. If
        this graph is a directed graph, an edge from vertex one to vertex two
        is added to this graph. If this graph is undirected, bidirectional
        connectivity is established.

        Args:
            vertex_one (str): Vertex one (source vertex in case of directed
                              graph).
            vertex_two (str): Vertex two (destination vertex in case of
                              directed graph).
            weight (int): The weight of the new edge. If this graph is
                          undirected, the wieght is applied to both
                          directions. This argument is optional - the
                          value 1 is used as default.
        """
        self._add_edge(vertex_one, vertex_two, weight)
        if self.graph_type is GraphType.UNDIRECTED:
            self._add_edge(vertex_two, vertex_one, weight) # pylint: disable=W1114
        self._weights.add(weight)

    def _add_edge(self, vertex_one: str, vertex_two: str, weight: int):
        if not vertex_one in self._adjacency_sets:
            self._adjacency_sets[vertex_one] = _AdjacencySet(vertex_one)
        if not vertex_two in self._adjacency_sets:
            self._adjacency_sets[vertex_two] = _AdjacencySet(vertex_two)
        self._adjacency_sets[vertex_one].add_edge(vertex_two, weight)

    def get_all_vertices(self, sort: bool = False) -> Tuple[str, ...]:
        """Creates and returns a new tuple containing names of all
        vertices involved in the graph represented by this object.

        Returns:
            Tuple[str, ...]: New tuple containing the names of all vertices
                             involved in the graph represented by this object.
                             If requested, the names are sorted in ascending
                             alphabetical order.
        """
        return tuple(sorted(self._adjacency_sets) if sort else self._adjacency_sets)

    def get_adjacent_vertices(self, vertex: str) -> Tuple[str, ...]:
        """Creates and returns a new tuple containing the names of vertices
        adjacent to the vertex with the given name.

        Args:
            vertex (str): The name of the vertex whose adjacent vertices are
            to be returned.

        Returns:
            Tuple[str, ...]: New tuple containing the names of vertices
                             adjacent to the given vertex.
        """
        if not vertex in self._adjacency_sets:
            message = f'Vertex with the name {vertex} not found.'
            raise ValueError(message)
        return self._adjacency_sets[vertex].get_adjacent_vertices()

    def get_edge_weight(self, vertex_one: str, vertex_two: str) -> int:
        """Returns the weight of the edge connecting the given pair of
        vertices.

        Args:
            vertex_one (str): The source vertex of the edge whose weight is
                              to be returned.
            vertex_two (str): The destination vertex of the edge whose weight
                              is to be returned.

        Returns:
            int: The weight of the edge connecting the given pair of vertices.
        """
        self._raise_error_if_vertex_unknown(vertex_one)
        self._raise_error_if_vertex_unknown(vertex_two)
        return self._adjacency_sets[vertex_one].get_edge_weight(vertex_two)

    def _raise_error_if_vertex_unknown(self, vertex: str):
        if not vertex in self._adjacency_sets:
            message = f'Vertex with the name {vertex} not found.'
            raise ValueError(message)

    def get_in_degree(self, vertex: str) -> int:
        """Returns the in-degree of the vertex with the given name.

        Args:
            vertex (str): The name of the vertex whose in-degree is to be
                          returned.

        Returns:
            int: The number of edges incident to the vertex with the given
                 name.
        """
        result = 0
        for name in self._adjacency_sets:
            adjacency_set = self._adjacency_sets[name]
            if vertex in adjacency_set:
                result = result + 1
        return result
