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

from abc import ABC, abstractproperty

from pytest import raises

from graphlib.graph import AdjacencyMatrixGraph, AdjacencySetGraph, GraphType
from graphlib.jsondef import build_adjacency_matrix_graph_from_json_string
from graphlib.jsondef import build_adjacency_set_graph_from_json_string

class AbstractGraphBuildingTestFixture(ABC):

    @abstractproperty
    def tested_function(self):
        raise NotImplementedError

    @abstractproperty
    def expected_graph_class(self):
        raise NotImplementedError

    def test_directed_weighted_graph_is_built_properly_from_valid_definition(self):
        json_string = """
{
    "graphType": "DIRECTED",
    "edges": [
        {
            "start": "A",
            "destination": "B",
            "weight": 3
        }, {
            "start": "A",
            "destination": "C",
            "weight": 5
        }, {
            "start": "B",
            "destination": "D",
            "weight": 4
        }, {
            "start": "C",
            "destination": "D",
            "weight": 2
        }, {
            "start": "D",
            "destination": "E",
            "weight": 6
        }
    ]
}
"""
        graph = self.tested_function(json_string)

        assert isinstance(graph, self.expected_graph_class)
        assert graph.graph_type == GraphType.DIRECTED
        assert graph.get_edge_weight('A', 'B') == 3
        assert graph.get_edge_weight('A', 'C') == 5
        assert graph.get_edge_weight('B', 'D') == 4
        assert graph.get_edge_weight('C', 'D') == 2
        assert graph.get_edge_weight('D', 'E') == 6

        for start, destination in ('B', 'A'), ('C', 'A'), ('D', 'B'), ('D', 'C'), ('E', 'D'):
            with raises(ValueError):
                graph.get_edge_weight(start, destination)

    def test_undirected_weighted_graph_is_built_properly_from_valid_definition(self):
        json_string = """
{
    "graphType": "UNDIRECTED",
    "edges": [
        {
            "start": "A",
            "destination": "B",
            "weight": 3
        }, {
            "start": "A",
            "destination": "C",
            "weight": 5
        }, {
            "start": "B",
            "destination": "D",
            "weight": 4
        }, {
            "start": "C",
            "destination": "D",
            "weight": 2
        }, {
            "start": "D",
            "destination": "E",
            "weight": 6
        }
    ]
}
"""
        graph = self.tested_function(json_string)

        assert isinstance(graph, self.expected_graph_class)
        assert graph.graph_type == GraphType.UNDIRECTED
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

    def test_directed_unweighted_graph_is_parsed_properly_from_valid_definition(self):
        json_string = """
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
        graph = self.tested_function(json_string)

        assert isinstance(graph, self.expected_graph_class)
        assert graph.graph_type == GraphType.DIRECTED
        for start, destination in ('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E'):
            assert graph.get_edge_weight(start, destination) == 1
            with raises(ValueError):
                graph.get_edge_weight(destination, start)

    def test_undirected_unweighted_graph_is_parsed_properly_from_valid_definition(self):
        json_string = """
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
        graph = self.tested_function(json_string)

        assert isinstance(graph, self.expected_graph_class)
        assert graph.graph_type == GraphType.UNDIRECTED
        for vertex_one, vertex_two in ('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E'):
            assert graph.get_edge_weight(vertex_one, vertex_two) == 1
            assert graph.get_edge_weight(vertex_two, vertex_one) == 1

    def test_json_definition_without_graph_type_leads_to_error(self):
        json_data = """
{
    "edges": [
        {
            "start": "A",
            "destination": "B",
            "weight": 3
        }, {
            "start": "B",
            "destination": "C",
            "weight": 4
        }
    ]
}
"""

        with raises(ValueError, match='Undefined graph type.'):
            self.tested_function(json_data)

    def test_json_definition_with_invalid_graph_type_leads_to_error(self):
        json_data = """
{
    "graphType": "DUMB",
    "edges": [
        {
            "start": "A",
            "destination": "B",
            "weight": 3
        }, {
            "start": "B",
            "destination": "C",
            "weight": 4
        }
    ]
}
"""

        with raises(ValueError, match='Invalid graph type: DUMB.'):
            self.tested_function(json_data)

    def test_json_definition_without_edge_list_leads_to_error(self):
        json_data = """
{
    "graphType": "DIRECTED"
}
"""

        with raises(ValueError, match='Missing edge list.'):
            self.tested_function(json_data)

    def test_json_definition_with_empty_edge_list_leads_to_error(self):
        json_data = """
{
    "graphType": "DIRECTED",
    "edges": []
}
"""

        with raises(ValueError, match='Empty edge list.'):
            self.tested_function(json_data)

    def test_json_definition_with_missing_start_vertex_leads_to_error(self):
        json_data = """
{
    "graphType": "DIRECTED",
    "edges": [
        {
            "destination": "B",
            "weight": 3
        }, {
            "start": "B",
            "destination": "C",
            "weight": 4
        }
    ]
}
"""

        with raises(ValueError, match='Edge with undefined start vertex.'):
            self.tested_function(json_data)

    def test_json_definition_with_missing_destination_vertex_leads_to_error(self):
        json_data = """
{
    "graphType": "DIRECTED",
    "edges": [
        {
            "start": "A",
            "destination": "B",
            "weight": 3
        }, {
            "start": "B",
            "weight": 4
        }
    ]
}
"""

        with raises(ValueError, match='Edge with undefined destination vertex.'):
            self.tested_function(json_data)

    def test_json_definition_with_invalid_edge_weight_leads_to_error(self):
        json_data = """
{
    "graphType": "DIRECTED",
    "edges": [
        {
            "start": "A",
            "destination": "B",
            "weight": "X"
        }
    ]
}
"""

        with raises(ValueError, match='Invalid weight: X.'):
            self.tested_function(json_data)

    def test_json_definition_with_negative_edge_weight_leads_to_error(self):
        json_data = """
{
    "graphType": "DIRECTED",
    "edges": [
        {
            "start": "A",
            "destination": "B",
            "weight": -1
        }
    ]
}
"""

        with raises(ValueError, match='Invalid weight: -1.'):
            self.tested_function(json_data)

    def test_json_definition_with_edge_weight_equal_to_zero_leads_to_error(self):
        json_data = """
{
    "graphType": "DIRECTED",
    "edges": [
        {
            "start": "A",
            "destination": "B",
            "weight": 0
        }
    ]
}
"""

        with raises(ValueError, match='Invalid weight: 0.'):
            self.tested_function(json_data)


class TestAdjacencySetGraphBuilding(AbstractGraphBuildingTestFixture):

    @property
    def tested_function(self):
        return build_adjacency_set_graph_from_json_string

    @property
    def expected_graph_class(self):
        return AdjacencySetGraph


class TestAdjacencyMatrixGraphBuilding(AbstractGraphBuildingTestFixture):

    @property
    def tested_function(self):
        return build_adjacency_matrix_graph_from_json_string

    @property
    def expected_graph_class(self):
        return AdjacencyMatrixGraph

