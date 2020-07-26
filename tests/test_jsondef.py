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

from io import StringIO
import json

from graphlib.jsondef import build_adjacency_matrix_graph, build_adjacency_set_graph

class TestGraphBuilding:

    def _directed_weighted_graph_json_definition(self):
        json_data = """
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
        return StringIO(json_data)

    def _undirected_weighted_graph_json_definition(self):
        json_data = """
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
        return StringIO(json_data)

    def _directed_unweighted_graph_json_definition(self):
        json_data = """
        """
        return StringIO(json_data)

    def _undirected_unweighted_graph_json_definition(self):
        json_data = """
        """
        return StringIO(json_data)

    # TODO:
    # - invalid graph type
    # - invalid edge weight
    # - missing start vertex
    # - missing destination vertex
