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
from typing import Dict, Sequence, Tuple

from graphlib.graph import AbstractGraph, GraphType
from graphlib.util import PriorityQueue, QueueableItem


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

    for vertex in graph.get_sorted_vertices():
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
class Edge:
    """Immutable structure representing a single edge of a shortest path
    search result (see :class: ShortestPathSearchResult) or a minimum
    spanning tree (see :class: MinimumSpanningTree).
    """
    start: str
    destination: str
    weight: int


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


@dataclass(frozen=True)
class MinimumSpanningTree:
    """Immutable structure whose instances will representing minimum spanning
    trees.

    The start attribute carries the vertex where the search whose result is
    represented by this object started.
    """
    search_start: str
    edges: Tuple[Edge, ...]

    @property
    def overall_weight(self):
        """The overall weight of the minimum spanning represeted by this
        object.

        In other words, the sum of the weights of all edges comprising the
        minimum spanning tree.
        """
        return sum(map(lambda edge: edge.weight, self.edges))


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
        print(f'Distance table entry created for starting vertex {starting_vertex}')

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
            print(f'Vertex {vertex} already present, going to update its entry')
            result = self._entries[vertex].update(predecessor, distance)
            print(f'Updated entry: {self._entries[vertex]}')
            return result
        print(f'Vertex {vertex} not present yet, going to create a new entry')
        self._entries[vertex] = _DistanceTableEntry(vertex, predecessor, distance)
        print(f'Created entry: {self._entries[vertex]}')
        return True

    def backtrack_shortest_path(self,
                                request: ShortestPathSearchRequest) -> ShortestPathSearchResult:
        # TODO: we should also check if the request carries the same start
        # vertex as the one used to create this distance table
        graph = request.graph
        path = deque()
        destination: str = request.destination
        start: str = self._entries[destination].predecessor
        weight = graph.get_edge_weight(start, destination)
        while True:
            path.appendleft(Edge(start, destination, weight))
            destination = start
            start = self._entries[destination].predecessor
            if start == destination == request.start:
                break
            weight = graph.get_edge_weight(start, destination)
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
    explored_vertices = {request.start}
    queue = PriorityQueue()
    graph = request.graph

    for adjacent_vertex in request.graph.get_adjacent_vertices(request.start):
        weight = request.graph.get_edge_weight(request.start, adjacent_vertex)
        distance_table.update(adjacent_vertex, request.start, weight)
        item = QueueableItem(key=adjacent_vertex, priority=weight, value=weight)
        queue.enqueue(item)
        print(f'{adjacent_vertex} added to the queue')

    while not queue.empty():
        item = queue.dequeue()
        current_vertex = item.key
        current_vertex_distance_from_start = item.value
        explored_vertices.add(current_vertex)
        print(f'Adding vertex {current_vertex} to explored vertices')
        for adjacent_vertex in graph.get_adjacent_vertices(current_vertex):
            if adjacent_vertex in explored_vertices:
                print(f'Adjacent vertex {adjacent_vertex} already explored')
                continue
            print(f'Adjacent vertex {adjacent_vertex} not explored yet')
            weight = graph.get_edge_weight(current_vertex, adjacent_vertex)
            adjacent_vertex_distance_from_start = current_vertex_distance_from_start + weight
            print(f'Predecessor = {current_vertex}, distance from start = {current_vertex_distance_from_start}')
            if distance_table.update(adjacent_vertex, current_vertex, adjacent_vertex_distance_from_start):
                print(f'Distance table updated for {adjacent_vertex}')
                item = QueueableItem(key=adjacent_vertex, priority=adjacent_vertex_distance_from_start, value=adjacent_vertex_distance_from_start)
                queue.enqueue(item)
                print(f'{adjacent_vertex} added to the queue')

    return distance_table


def find_shortest_path(request: ShortestPathSearchRequest) -> ShortestPathSearchResult:
    """Finds and returns the shortest path from the given start vertex to the
    specified destination vertex in the given graph.

    Args:
        request (ShortestPathSearchRequest): Search request carrying the start
                                             and destination vertices as well
                                             as the graph in which the path is
                                             to be searched.

    Returns:
        ShortestPathSearchResult: The search result (i.e. the found shortest
                                  path).
    """
    if request.graph.is_weighted:
        distance_table = _build_weighted_distance_table(request)
    else:
        distance_table = _build_unweighted_distance_table(request)
    return distance_table.backtrack_shortest_path(request)
