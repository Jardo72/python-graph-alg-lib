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
from copy import copy
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
    """Immutable structure representing a single edge of the shortest path
    search result (see :class: ShortestPathSearchResult).
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


@dataclass
class _DistanceTableEntry:
    """Simple data-class representing a single entry of the distance table.
    """
    vertex: str
    predecessor: str
    distance: int

    def _update(self, predecessor: str, distance: int):
        if self.distance > distance:
            self.distance = distance
            self.predecessor = predecessor


_DistanceTable = Dict[str, _DistanceTableEntry]


def _build_distance_table(request: ShortestPathSearchRequest) -> _DistanceTable:
    distance_table: _DistanceTable = {
        request.start: _DistanceTableEntry(request.start, request.start, 0)
    }
    explored_vertices = {request.start}
    queue = PriorityQueue()
    graph = request.graph

    for adjacent_vertex in request.graph.get_adjacent_vertices(request.start):
        weight = request.graph.get_edge_weight(request.start, adjacent_vertex)
        distance_table_entry = _DistanceTableEntry(
            vertex=adjacent_vertex,
            predecessor=request.start,
            distance=weight)
        distance_table[adjacent_vertex] = distance_table_entry
        item = QueueableItem(key=adjacent_vertex, priority=weight, value=copy(distance_table_entry))
        queue.enqueue(item)

    while not queue.empty():
        item = queue.dequeue()
        current_vertex = item.key
        explored_vertices.add(current_vertex)
        adjacent_vertices = graph.get_adjacent_vertices(current_vertex)
        for adjacent_vertex in adjacent_vertices:
            if adjacent_vertex in explored_vertices:
                continue
            weight = graph.get_edge_weight(current_vertex, adjacent_vertex)

    return distance_table


def _backtrack_shortest_path(request: ShortestPathSearchRequest,
                             distance_table: _DistanceTable)-> ShortestPathSearchResult:
    graph = request.graph
    path = deque()
    destination: str = request.destination
    start: str = distance_table[destination].predecessor
    weight = graph.get_edge_weight(start, destination)
    while True:
        path.appendleft(Edge(start, destination, weight))
        destination = start
        start = distance_table[destination].predecessor
        if start == request.start:
            break
        weight = graph.get_edge_weight(start, destination)
    return ShortestPathSearchResult(tuple(path))


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
    distance_table = _build_distance_table(request)
    return _backtrack_shortest_path(request, distance_table)
