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

"""This module allows to read graph definitions from JSON files.
"""

from json import loads
from typing import Any, Dict, Sequence, Tuple

from graphlib.graph import AdjacencyMatrixGraph, AdjacencySetGraph, GraphType


def _read_graph_type(json_data: Dict[str, Any]) -> GraphType:
    if 'graphType' not in json_data:
        raise ValueError('Undefined graph type.')
    graph_type_as_string = json_data['graphType']
    try:
        return GraphType[graph_type_as_string]
    except KeyError:
        raise ValueError(f'Invalid graph type: {graph_type_as_string}.')


def _read_single_edge(json_data: Dict[str, Any]) -> Tuple[str, str, int]:
    if 'start' not in json_data:
        raise ValueError('Edge with undefined start vertex.')
    if 'destination' not in json_data:
        raise ValueError('Edge with undefined destination vertex.')
    start = json_data['start']
    destination = json_data['destination']
    if 'weight' not in json_data:
        weight = 1
    else:
        try:
            weight = int(json_data['weight'])
            if weight <= 0:
                raise ValueError()
        except ValueError:
            raise ValueError(f'Invalid weight: {json_data["weight"]}.')
    return (start, destination, weight)


def _read_edge_list(json_data: Dict[str, Any]) -> Sequence[Tuple[str, str, int]]:
    if 'edges' not in json_data:
        raise ValueError('Missing edge list.')
    result = [_read_single_edge(single_edge) for single_edge in json_data['edges']]
    if len(result) == 0:
        raise ValueError('Empty edge list.')
    return result


def build_adjacency_set_graph_from_json_string(json_string: str) -> AdjacencySetGraph:
    """Creates and returns a new adjacency set graph created according to the
    JSON definition represented by the given string.

    Args:
        json_string (str): String carrying the JSON definition of the graph to be
                           built.

    Returns:
        AdjacencySetGraph: The created graph.
    """
    json_data = loads(json_string)
    graph_type = _read_graph_type(json_data)
    graph = AdjacencySetGraph(graph_type)
    for start, destination, weight in _read_edge_list(json_data):
        graph.add_edge(start, destination, weight)
    return graph

def build_adjacency_set_graph_from_json_file(path: str) -> AdjacencySetGraph:
    """Creates and returns a new adjacency set graph created according to the
    JSON definition contained in the given file.

    Args:
        path (str): Path to the JSON file containing the graph definition to be
                    read.

    Returns:
        AdjacencySetGraph: The created graph.
    """
    with open(path, 'r') as json_file:
        json_data = "".join(line.rstrip() for line in json_file)
        return build_adjacency_set_graph_from_json_string(json_data)


def build_adjacency_matrix_graph_from_json_string(json_string: str) -> AdjacencyMatrixGraph:
    """Creates and returns a new adjacency matrix graph created according to the
    JSON definition represented by the given string.

    This method ensures that the underlying adjacency matrix of the created graph
    has a capacity sufficient to represent the graph described by the given JSON
    definition.

    Args:
        json_string (str): String carrying the JSON definition of the graph to be
                           built.

    Returns:
        AdjacencyMatrixGraph: The created graph.
    """
    json_data = loads(json_string)
    graph_type = _read_graph_type(json_data)
    edge_list = _read_edge_list(json_data)
    max_vertex_count = 2 * len(edge_list)
    graph = AdjacencyMatrixGraph(max_vertex_count, graph_type)
    for start, destination, weight in edge_list:
        graph.add_edge(start, destination, weight)
    return graph


def build_adjacency_matrix_graph_from_json_file(path: str) -> AdjacencyMatrixGraph:
    """Creates and returns a new adjacency matrix graph created according to the given
    JSON definition contained in the given file.

    This method ensures that the underlying adjacency matrix of the created graph
    has a capacity sufficient to represent the graph described by the given JSON
    definition.

    Args:
        path (str): Path to the JSON file containing the graph definition to be
                    read.
    Returns:
        AdjacencyMatrixGraph: The created graph.
    """
    with open(path, 'r') as json_file:
        json_data = "".join(line.rstrip() for line in json_file)
        return build_adjacency_matrix_graph_from_json_string(json_data)
