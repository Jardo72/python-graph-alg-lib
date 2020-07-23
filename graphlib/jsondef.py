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

from json import load
from typing import Any, Dict, Sequence, Tuple

from graphlib.graph import AdjacencyMatrixGraph, AdjacencySetGraph, GraphType


def _read_graph_type(json_data: Dict[str, Any]) -> GraphType:
    # TODO: error handling is missing
    graph_type_as_string = json_data['graphType']
    return GraphType[graph_type_as_string]


def _read_single_edge(json_data: Dict[str, Any]) -> Tuple[str, str, int]:
    # TODO: error handling is missing
    start = json_data['start']
    destination = json_data['destination']
    weight = int(json_data['weight'])
    return (start, destination, weight)


def _read_edge_list(json_data: Dict[str, Any]) -> Sequence[Tuple[str, str, int]]:
    return [_read_single_edge(single_edge) for single_edge in json_data['edges']]


def build_adjacency_set_graph(path: str) -> AdjacencySetGraph:
    """Creates and returns a new adjacency set graph created according to the given
    JSON definition.

    Args:
        path (str): [description]

    Returns:
        AdjacencySetGraph: The created graph.
    """
    with open(path, 'r') as json_file:
        json_data = load(json_file)
        graph_type = _read_graph_type(json_data)
        graph = AdjacencySetGraph(graph_type)
        for start, destination, weight in _read_edge_list(json_data):
            graph.add_edge(start, destination, weight)
        return graph


def build_adjacency_matrix_graph(path: str) -> AdjacencyMatrixGraph:
    """Creates and returns a new adjacency set graph created according to the given
    JSON definition.

    Args:
        path (str): [description]

    Returns:
        AdjacencyMatrixGraph: The created graph.
    """
    with open(path, 'r') as json_file:
        json_data = load(json_file)
        graph_type = _read_graph_type(json_data)
        # TODO:
        # - the hardcoded vertex count should be improved
        graph = AdjacencyMatrixGraph(100, graph_type)
        for start, destination, weight in _read_edge_list(json_data):
            graph.add_edge(start, destination, weight)
        return graph
