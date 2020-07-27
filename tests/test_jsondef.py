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

"""Unit tests for the graphlib.jsondef module.
"""

from graphlib.graph import AdjacencySetGraph

from pytest import raises

from graphlib.jsondef import build_adjacency_set_graph_from_json_string

class TestGraphBuilding:

    def _directed_weighted_graph_json_definition(self):
        return """
{
    "graphType": "DIRECTED",
    "edges": [
        {
            "start": "A",
            "destination": "B",
            "weight": "3"
        }, {
            "start": "A",
            "destination": "C",
            "weight": "5"
        }, {
            "start": "B",
            "destination": "D",
            "weight": "4"
        }, {
            "start": "C",
            "destination": "D",
            "weight": "2"
        }, {
            "start": "D",
            "destination": "E",
            "weight": "6"
        }
    ]
}
"""

    def _undirected_weighted_graph_json_definition(self):
        return """
{
    "graphType": "UNDIRECTED",
    "edges": [
        {
            "start": "A",
            "destination": "B",
            "weight": "3"
        }, {
            "start": "A",
            "destination": "C",
            "weight": "5"
        }, {
            "start": "B",
            "destination": "D",
            "weight": "4"
        }, {
            "start": "C",
            "destination": "D",
            "weight": "2"
        }, {
            "start": "D",
            "destination": "E",
            "weight": "6"
        }
    ]
}
"""

    def _directed_unweighted_graph_json_definition(self):
        return """
{
    "graphType": "DIRECTED",
    "edges": [
        {
            "start": "A",
            "destination": "B"
        }, {
            "start": "A",
            "destination": "C"
        }, {
            "start": "B",
            "destination": "D"
        }, {
            "start": "C",
            "destination": "D"
        }, {
            "start": "D",
            "destination": "E"
        }
    ]
}
        """

    def _undirected_unweighted_graph_json_definition(self):
        return """
{
    "graphType": "UNDIRECTED",
    "edges": [
        {
            "start": "A",
            "destination": "B"
        }, {
            "start": "A",
            "destination": "C"
        }, {
            "start": "B",
            "destination": "D"
        }, {
            "start": "C",
            "destination": "D"
        }, {
            "start": "D",
            "destination": "E"
        }
    ]
}
        """

    def _missing_graph_type_json_definition(self):
        return """
{
    "edges": [
        {
            "start": "A",
            "destination": "B",
            "weight": "3"
        }, {
            "start": "B",
            "destination": "C",
            "weight": "4"
        }
    ]
}
        """

    def _invalid_graph_type_json_definition(self):
        return """
{
    "graphType": "DUMB",
    "edges": [
        {
            "start": "A",
            "destination": "B",
            "weight": "3"
        }, {
            "start": "B",
            "destination": "C",
            "weight": "4"
        }
    ]
}
        """

    def test_directed_weighted_graph_is_parsed_properly(self):
        json_string = self._directed_weighted_graph_json_definition()
        graph = build_adjacency_set_graph_from_json_string(json_string)

        assert isinstance(graph, AdjacencySetGraph)
        assert graph.get_edge_weight('A', 'B') == 3
        assert graph.get_edge_weight('A', 'C') == 5
        assert graph.get_edge_weight('B', 'D') == 4
        assert graph.get_edge_weight('C', 'D') == 2
        assert graph.get_edge_weight('D', 'E') == 6

        for start, destination in ('B', 'A'), ('C', 'A'), ('D', 'B'), ('D', 'C'), ('E', 'D'):
            with raises(ValueError):
                graph.get_edge_weight(start, destination)

    def test_undirected_weighted_graph_is_parsed_properly(self):
        json_string = self._undirected_weighted_graph_json_definition()
        graph = build_adjacency_set_graph_from_json_string(json_string)

        assert isinstance(graph, AdjacencySetGraph)
        assert graph.get_edge_weight('A', 'B') == 3
        assert graph.get_edge_weight('B', 'A') == 3
        assert graph.get_edge_weight('A', 'C') == 5
        assert graph.get_edge_weight('C', 'A') == 5
        assert graph.get_edge_weight('B', 'D') == 4
        assert graph.get_edge_weight('D', 'B') == 4
        assert graph.get_edge_weight('C', 'D') == 2
        assert graph.get_edge_weight('D', 'C') == 2
        assert graph.get_edge_weight('D', 'E') == 6
        assert graph.get_edge_weight('E', 'D') == 6

    def test_directed_unweighted_graph_is_parsed_properly(self):
        json_string = self._directed_unweighted_graph_json_definition()
        graph = build_adjacency_set_graph_from_json_string(json_string)

        assert isinstance(graph, AdjacencySetGraph)
        for start, destination in ('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E'):
            assert graph.get_edge_weight(start, destination) == 1
            with raises(ValueError):
                graph.get_edge_weight(destination, start)

    def test_undirected_unweighted_graph_is_parsed_properly(self):
        json_string = self._undirected_unweighted_graph_json_definition()
        graph = build_adjacency_set_graph_from_json_string(json_string)

        assert isinstance(graph, AdjacencySetGraph)
        for vertex_one, vertex_two in ('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E'):
            assert graph.get_edge_weight(vertex_one, vertex_two) == 1
            assert graph.get_edge_weight(vertex_two, vertex_one) == 1

    # TODO:
    # - missing graph type
    # - invalid graph type
    # - missing edge weight (default 1)
    # - invalid edge weight
    # - missing start vertex
    # - missing destination vertex
