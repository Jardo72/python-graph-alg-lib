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

"""This module provides methods allowing to dump various data structures
like a graph or a result of shortest path search.
"""
from graphlib.algorithms import MinimumSpanningTreeSearchResult, ShortestPathSearchResult
from graphlib.graph import AbstractGraph

def dump_graph(graph: AbstractGraph, output):
    """Dumps the vertices and edges of the given graph to given text output.

    The dump is generated in a structured way, and it also includes the weights
    of the edges.

    Args:
        graph (AbstractGraph): The graph to be dumped.
        output:                The text output the dump is to be written to.
                               It can be a file, sys.stdout, or an io.StringIO
                               instance.
    """
    weighted = 'YES' if graph.is_weighted else 'NO'
    output.write('\n')
    output.write(f'Graph type: {graph.graph_type}\n')
    output.write(f'Weighted: {weighted}\n')
    output.write(f'Vertices (totally {graph.vertex_count}):\n')
    for current_vertex in graph.get_all_vertices(sort=True):
        output.write(f' - {current_vertex}\n')
    output.write('Edges:\n')
    for current_vertex in graph.get_all_vertices(sort=True):
        for adjacent_vertex in graph.get_adjacent_vertices(current_vertex):
            weight = graph.get_edge_weight(current_vertex, adjacent_vertex)
            output.write(f' - {current_vertex} -> {adjacent_vertex} (weight = {weight})\n')


def dump_shortest_path(shortest_path: ShortestPathSearchResult, output):
    """Dumps the given shortest path to the given text output.

    The dump provides information about the start and the destination of the
    path, the overall distance, and about the individual edges comprising the
    path.

    Args:
        shortest_path (ShortestPathSearchResult): The shortest path to be dumped.
        output:                                   The text output the dump is to
                                                  be written to. It can be a file,
                                                  sys.stdout, or an io.StringIO
                                                  instance.
    """
    output.write('\n')
    output.write(f'Shortest path from {shortest_path.start} to {shortest_path.destination}\n')
    output.write(f'Overall distance {shortest_path.overall_distance}\n')
    output.write('Path:\n')
    for edge in shortest_path.path:
        output.write(f' - {edge.start} -> {edge.destination} (weight = {edge.weight})\n')


def dump_minimum_spanning_tree(minimum_spanning_tree: MinimumSpanningTreeSearchResult, output):
    """Dumps the given minimum spanning tree to the given text output.

    The dump provides information about the starting vertex of the search
    that has found the given minimum spanning tree, plus the overall weight.

    Args:
        shortest_path (ShortestPathSearchResult): The minimum spanning spanning
                                                  tree to be dumped.
        output:                                   The text output the dump is to
                                                  be written to. It can be a file,
                                                  sys.stdout, or an io.StringIO
                                                  instance.
    """
    output.write('\n')
    if minimum_spanning_tree.search_start:
        output.write(f'Minimum spanning tree (search start {minimum_spanning_tree.search_start})\n')
    else:
        output.write('Minimum spanning tree\n')
    output.write(f'Search algorithm {minimum_spanning_tree.algorithm}\n')
    output.write(f'Overall weight {minimum_spanning_tree.overall_weight}\n')
    output.write('Edges:\n')
    for edge in minimum_spanning_tree.edges:
        output.write(f' - {edge.start} -> {edge.destination} (weight = {edge.weight})\n')
