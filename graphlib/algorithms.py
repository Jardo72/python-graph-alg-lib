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

"""This module provides various implementations of graph algorithms.
"""

from collections import deque
from dataclasses import dataclass
from enum import Enum, unique
from typing import Dict, Optional, Sequence, Tuple

from graphlib.graph import AbstractGraph, Edge, GraphType
from graphlib.util import QueueableItem, RepriorizablePriorityQueue, SimplePriorityQueue
from graphlib.util import UnionFind


def sort_topologically(graph: AbstractGraph) -> Sequence[str]:
    """Creates and returns a new sequence containing topologically sorted
    vertices of the given graph.

    Args:
        graph (AbstractGraph): The graph whose vertices are to be toplogically
                               sorted.

    Returns:
        Sequence[str]: Collection of vertices sorted in topological order.
    """
    if graph.graph_type == GraphType.UNDIRECTED:
        message = 'Topological sort can only be applied to directed graphs.'
        raise ValueError(message)
    queue: deque = deque()
    in_degree_map: Dict[str, int] = {}

    for vertex in graph.get_all_vertices():
        in_degree_map[vertex] = graph.get_in_degree(vertex)
        if in_degree_map[vertex] == 0:
            queue.append(vertex)

    if len(queue) == 0:
        message = 'Topological sort can only be applied to acyclic graphs.'
        raise ValueError(message)

    result = []
    while len(queue) > 0:
        vertex = queue.popleft()
        result.append(vertex)
        for neighbor in graph.get_adjacent_vertices(vertex):
            in_degree_map[neighbor] -= 1
            if in_degree_map[neighbor] == 0:
                queue.append(neighbor)

    return result


@dataclass(frozen=True)
class ShortestPathSearchRequest:
    """Immutable structure representing a request to search the shortest path
    from the given start vertex to the specified destination vertex in the
    given graph.
    """
    graph: AbstractGraph
    start: str
    destination: str


@dataclass(frozen=True)
class ShortestPathSearchResult:
    """Immutable structure representing the result of a shortest-path
    search.
    """
    path: Tuple[Edge, ...]

    @property
    def start(self) -> str:
        """The start edge of the found shortest path.
        """
        return self.path[0].start

    @property
    def destination(self) -> str:
        """The destination edge of the found shortest path.
        """
        return self.path[-1].destination

    @property
    def overall_distance(self) -> int:
        """The overall distance of the found shortest path.

        In other words, the sum of the weights of all edges comprising the
        found shortest path.
        """
        return sum(map(lambda edge: edge.weight, self.path))


@unique
class MinimumSpanningTreeAlgorithm(Enum):
    """Enumeration defining types of minumum spanning tree algorithms.
    """

    PRIM = 1

    KRUSKAL = 2


@dataclass(frozen=True)
class MinimumSpanningTreeSearchRequest:
    """Immutable structure whose instances represent requests to find a minimum
    spanning tree.

    The search start attribute carries the vertex where the search has to start.
    The attribute is optional - it should not be used for algorithms not using any
    start (e.g. Kruskal's algorithm).
    """
    graph: AbstractGraph
    algorithm: MinimumSpanningTreeAlgorithm
    search_start: Optional[str] = None


@dataclass(frozen=True)
class MinimumSpanningTreeSearchResult:
    """Immutable structure whose instance represents the result of a search for
    minimum spanning tree.

    The search start attribute carries the vertex where the search whose result
    is represented by this object started. The attribute is optional - it is not
    used for algorithms not using any start (e.g. Kruskal's algorithm).
    """
    algorithm: MinimumSpanningTreeAlgorithm
    search_start: Optional[str]
    edges: Tuple[Edge, ...]

    @property
    def overall_weight(self):
        """The overall weight of the minimum spanning represeted by this
        object.

        In other words, the sum of the weights of all edges comprising the
        minimum spanning tree.
        """
        return sum(map(lambda edge: edge.weight, self.edges))

    def __contains__(self, edge: Edge) -> bool:
        """Verifies whether the given edge is part of the minimum spanning tree
        represented by this object.

        Args:
            edge (Edge): The edge whose presence in this minimum spanning tree is
                         to be verified.

        Returns:
            bool: True if and only if the given edge is contained in this minimum
                  spanning tree; False otherwise.
        """
        return edge in self.edges

    def __len__(self) -> int:
        """Returns the number of edges forming this minimum spanning tree.

        Returns:
            int: The number of edges contained in the minimum spanning tree
                 represented by this object.
        """
        return len(self.edges)


@dataclass
class _DistanceTableEntry:
    """Simple data-class representing a single entry of the distance table.
    """
    vertex: str
    predecessor: str
    distance_from_start: int

    def update(self, predecessor: str, distance_from_start: int) -> bool:
        """Updates the predecessor and the distance from start of this entry to
        the given values, assumed the given distance from start is less than the
        current distance from start.

        Args:
            predecessor (str): [description]
            distance_from_start (int): [description]

        Returns:
            bool: True if this entry has been updated; False if the updated has
                  been ignored (i.e. the given distance from start is not less
                  than the current distance from start).
        """
        if self.distance_from_start > distance_from_start:
            self.distance_from_start = distance_from_start
            self.predecessor = predecessor
            return True
        return False


class _DistanceTable:
    """Distance table supporting the implementation of Dijkstra's algorithm.
    """

    def __init__(self, starting_vertex: str):
        """Constructs a new distance table with the given starting vertex.

        The constructed distance table contains just a single entry. The entry
        concerns the given starting vertex, for which the distance is equal to
        zero, and the starting vertex also is its own predecessor.

        Args:
            starting_vertex (str): The starting vertex from which the distances
                                   of other vertices will be calculated.
        """
        self._entries: Dict[str, _DistanceTableEntry] = {
            starting_vertex: _DistanceTableEntry(starting_vertex, starting_vertex, 0)
        }
        self._starting_vertex = starting_vertex

    def get_distance_from_start(self, vertex: str) -> int:
        """Returns the currently known shortest distance of the given vertex from
        the start vertex specified upon the creation of this distance table.

        The returned distance is not necessarily the shortest distance. It just
        reflects the current state of the search, so it can happen that a shorter
        path will be found if the search will continue.

        Args:
            vertex (str): The vertex whose shortest distance from the startinig vertex
                          is to be returned.

        Raises:
            ValueError: If this distance table does not contain any entry for the
                        the given vertex.

        Returns:
            int: The desired shortest distance.
        """
        entry = self._get_entry(vertex)
        return entry.distance_from_start

    def get_predecessor(self, vertex: str) -> str:
        """Returns the predecessor vertex of the given vertex in the currently
        known shortest path from the start vertex specified upon the creation of
        this distance table to the given vertex.

        Args:
            vertex (str): The vertex whose predecessor is to be returned.

        The returned predecessor is not necessarily the predecessor in the shortest
        path. It just reflects the current state of the search, so it can happen that
        a shorter path will be found if the search will continue.

        Raises:
            ValueError: If this distance table does not contain any entry for the
                        the given vertex.

        Returns:
            str: The desired predecessor.
        """
        entry = self._get_entry(vertex)
        return entry.predecessor

    def _get_entry(self, vertex: str) -> _DistanceTableEntry:
        if vertex not in self._entries:
            message = f'No distance table entry found for the vertex {vertex}.'
            raise ValueError(message)
        return self._entries[vertex]

    def update(self, vertex: str, predecessor: str, distance: int) -> bool:
        """Updates the entry for the given vertex with the given distance and
        predecessor (assumed the newly discovered path is shorter than any other
        path discovered so far).

        Args:
            vertex (str): The vertex whose entry is to be updated.
            predecessor (str): The predecessor through which a path with the
                               given distance is possible.
            distance (int): The distance of the newly discovered path.

        Returns:
            bool: True if the entry for the given vertex has been updated (i.e.
                  the newly discovered path is shorter that any other path
                  discovered so far); False otherwise.
        """
        if vertex in self._entries:
            result = self._entries[vertex].update(predecessor, distance)
            return result
        self._entries[vertex] = _DistanceTableEntry(vertex, predecessor, distance)
        return True

    def backtrack_shortest_path(self, destination: str) -> ShortestPathSearchResult:
        """Backtracks the shortest path from the starting vertex this distance table
        has been initialized with, to the given destination vertex.

        Args:
            destination (str): The destination vertex of the path to be backtracked.

        Returns:
            ShortestPathSearchResult: The result of the backtracking.
        """
        if destination not in self._entries:
            message = f'There is no path from {self._starting_vertex} to {destination}.'
            raise ValueError(message)

        path = deque()
        predecessor: str = self._entries[destination].predecessor
        destination_distance = self._entries[destination].distance_from_start
        predecessor_distance = self._entries[predecessor].distance_from_start
        weight = destination_distance - predecessor_distance
        while True:
            path.appendleft(Edge(predecessor, destination, weight))
            destination = predecessor
            predecessor = self._entries[destination].predecessor
            if predecessor == destination == self._starting_vertex:
                break
            destination_distance = self._entries[destination].distance_from_start
            predecessor_distance = self._entries[predecessor].distance_from_start
            weight = destination_distance - predecessor_distance
        return ShortestPathSearchResult(tuple(path))

    def __contains__(self, vertex: str) -> bool:
        """Verifies whether this distance table contains an entry for the given
        vertex.

        This method overloads the in operator.

        Args:
            vertex (str): The vertex for which the presence of entry in this
                          distance table is to be verified.

        Returns:
            bool: True if this distance table contains an entry for the given
                  vertex; False otherwise.
        """
        return vertex in self._entries


def _build_unweighted_distance_table(request: ShortestPathSearchRequest) -> _DistanceTable:
    distance_table = _DistanceTable(request.start)
    explored_vertices = {request.start}
    graph = request.graph
    queue = deque()

    for adjacent_vertex in request.graph.get_adjacent_vertices(request.start):
        distance_table.update(adjacent_vertex, request.start, 1)
        queue.append(adjacent_vertex)

    while len(queue) > 0:
        current_vertex = queue.popleft()
        current_distance = distance_table.get_distance_from_start(current_vertex)
        explored_vertices.add(current_vertex)
        for adjacent_vertex in graph.get_adjacent_vertices(current_vertex):
            if adjacent_vertex in explored_vertices:
                continue
            distance_from_start = current_distance + 1
            distance_table.update(adjacent_vertex, current_vertex, distance_from_start)
            queue.append(adjacent_vertex)

    return distance_table


def _build_weighted_distance_table(request: ShortestPathSearchRequest) -> _DistanceTable:
    distance_table = _DistanceTable(request.start)
    queue = RepriorizablePriorityQueue()
    explored_vertices = {request.start}
    graph = request.graph

    for adjacent_vertex in request.graph.get_adjacent_vertices(request.start):
        weight = request.graph.get_edge_weight(request.start, adjacent_vertex)
        distance_table.update(adjacent_vertex, request.start, weight)
        item = QueueableItem(key=adjacent_vertex, priority=weight, value=weight)
        queue.enqueue(item)

    while queue.is_not_empty():
        item = queue.dequeue()
        current_vertex = item.key
        current_distance_from_start = item.value
        explored_vertices.add(current_vertex)
        for adjacent_vertex in graph.get_adjacent_vertices(current_vertex):
            if adjacent_vertex in explored_vertices:
                continue
            weight = graph.get_edge_weight(current_vertex, adjacent_vertex)
            adjacent_distance_from_start = current_distance_from_start + weight
            if distance_table.update(adjacent_vertex, current_vertex, adjacent_distance_from_start):
                item = QueueableItem(key=adjacent_vertex,
                                     priority=adjacent_distance_from_start,
                                     value=adjacent_distance_from_start)
                queue.enqueue(item)

    return distance_table


def find_shortest_path(request: ShortestPathSearchRequest) -> ShortestPathSearchResult:
    """Finds and returns the shortest path from the given start vertex to the
    specified destination vertex in the given graph.

    This method can be used for unweighted as well as for weighted graphs. Depending
    on whether the given graph is unweighted or weighted, an appropriate algorithm is
    used.

    Args:
        request (ShortestPathSearchRequest): Search request carrying the start
                                             and destination vertices as well
                                             as the graph in which the path is
                                             to be searched.

    Returns:
        ShortestPathSearchResult: The search result (i.e. the found shortest
                                  path from the start to the destination specified
                                  by the given search request).
    """
    if request.graph.is_weighted:
        distance_table = _build_weighted_distance_table(request)
    else:
        distance_table = _build_unweighted_distance_table(request)
    return distance_table.backtrack_shortest_path(request.destination)


class _KruskalsAlgorithmSupport:
    """Internal helper class supporting the implementation of Kruskal's minimum spanning
    tree algorithm.
    """

    def __init__(self, vertex_count: int):
        """Constructs a new instance of Kruskal's algorithm support for a graph with the
        given number of vertices.

        Args:
            vertex_count (int): Number of vertices involved in the graph for which the
                                minimum spanning tree is going to be searched.
        """
        self._sequence = 0
        self._vertex_mapping: Dict[str, int] = {}
        self._union_find = UnionFind(vertex_count)

    def _get_vertex_index(self, vertex: str) -> int:
        if vertex not in self._vertex_mapping:
            new_index = self._sequence
            self._sequence += 1
            self._vertex_mapping[vertex] = new_index
            return new_index
        return self._vertex_mapping[vertex]

    def are_connected(self, vertex_one: str, vertex_two: str) -> bool:
        """Verifies whethet the given pair of vertices has been already connected.

        Args:
            vertex_one (str): First of the two vertices to be verified.
            vertex_two (str): Second of the two vertices to be verified.

        Returns:
            bool: True if the two vertices have been already connected; False if the
                  two vertices have not been connected yet.
        """
        vertex_one_index = self._get_vertex_index(vertex_one)
        vertex_two_index = self._get_vertex_index(vertex_two)
        subset_one = self._union_find.find_subset(vertex_one_index)
        subset_two = self._union_find.find_subset(vertex_two_index)
        return subset_one == subset_two

    def connect(self, vertex_one: str, vertex_two: str):
        """Establishes connection between the given pair of vertices.

        Args:
            vertex_one (str): First of the two vertices to be connected.
            vertex_two (str): Second of the two vertices to be connected.
        """
        vertex_one_index = self._get_vertex_index(vertex_one)
        vertex_two_index = self._get_vertex_index(vertex_two)
        self._union_find.union(vertex_one_index, vertex_two_index)

    def has_disconnected_vertex(self) -> bool:
        """Verifies whether there is still at least one disconnected vertex.

        If all vertices have been already connected, the algorithm can stop. If there
        is at least one disconnected vertex, the algorithm has to continue.

        Returns:
            bool: True if there is at least one disconnected vertex; False otherwise.
        """
        return self._union_find.subset_count > 1


def _find_mst_prim(request: MinimumSpanningTreeSearchRequest) -> MinimumSpanningTreeSearchResult:
    graph = request.graph
    explored_vertices = {request.search_start}
    queue = SimplePriorityQueue()
    result = set()

    for edge in graph.get_outgoing_edges(request.search_start):
        queue.enqueue(edge.weight, edge)

    while queue.is_not_empty() and len(explored_vertices) < graph.vertex_count:
        current_edge = queue.dequeue()
        current_vertex = current_edge.destination
        if current_vertex in explored_vertices:
            continue
        explored_vertices.add(current_vertex)
        result.add(current_edge)
        for adjacent_edge in graph.get_outgoing_edges(current_vertex):
            queue.enqueue(adjacent_edge.weight, adjacent_edge)

    return MinimumSpanningTreeSearchResult(request.algorithm, request.search_start, tuple(result))


def _find_mst_kruskal(request: MinimumSpanningTreeSearchRequest) -> MinimumSpanningTreeSearchResult:
    algorithm_support = _KruskalsAlgorithmSupport(request.graph.vertex_count)
    queue = SimplePriorityQueue()
    edge_set = set()
    for edge in request.graph.get_all_edges():
        if edge.start < edge.destination:
            queue.enqueue(edge.weight, edge)

    while queue.is_not_empty() and algorithm_support.has_disconnected_vertex():
        edge = queue.dequeue()
        if algorithm_support.are_connected(edge.start, edge.destination):
            continue
        algorithm_support.connect(edge.start, edge.destination)
        edge_set.add(edge)

    return MinimumSpanningTreeSearchResult(request.algorithm, None, tuple(edge_set))


def find_minimum_spanning_tree(request: MinimumSpanningTreeSearchRequest) -> MinimumSpanningTreeSearchResult:
    """Finds and returns a minimum spanning tree for the graph carries by the given
    search request.

    Args:
        request (MinimumSpanningTreeSearchRequest): Search request carrying the graph,
                                                    the search algorithm to be applied,
                                                    and the optional starting vertex (if
                                                    applicable for the algorithm to be
                                                    applied).

    Returns:
        MinimumSpanningTreeSearchResult: The search result.
    """
    if request.algorithm == MinimumSpanningTreeAlgorithm.PRIM:
        if request.search_start is None:
            message = "Prim's algorithm is requested, but starting vertex is undefined."
            raise ValueError(message)
        return _find_mst_prim(request)

    if request.algorithm == MinimumSpanningTreeAlgorithm.KRUSKAL:
        if request.search_start is not None:
            message = "Kruskal's algorithm is requested, but starting vertex is specified."
            raise ValueError(message)
        return _find_mst_kruskal(request)

    message = f'Unexpected minimum spanning tree algorithm: {request.algorithm}.'
    raise ValueError(message)
