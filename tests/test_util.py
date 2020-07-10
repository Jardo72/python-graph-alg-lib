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

"""Unit tests for the graphlib.util module.
"""

from pytest import raises

from graphlib.util import PriorityQueue


class TestPriorityQueue:
    """Collection of test methods exercising the class :class:
    graphlib.util.PriorityQueue.
    """

    def test_virgin_priority_queue_is_empty(self): # pylint: disable=R0201
        queue = PriorityQueue()
        assert queue.empty


    def test_priority_queue_with_elements_is_not_empty(self): # pylint: disable=R0201
        queue = PriorityQueue()

        queue.enqueue(4, 'D')
        assert not queue.empty()

        queue.enqueue(5, 'A')
        assert not queue.empty()

        queue.enqueue(3, 'B')
        assert not queue.empty()

        queue.dequeue()
        assert not queue.empty()

        queue.dequeue()
        assert not queue.empty()


    def test_priority_queue_after_removal_of_last_element_is_empty(self): # pylint: disable=R0201
        queue = PriorityQueue()

        queue.enqueue(5, 'A')
        queue.enqueue(3, 'B')
        queue.dequeue()
        queue.enqueue(4, 'C')
        queue.dequeue()
        queue.dequeue()
        assert queue.empty()

        queue.enqueue(2, 'D')
        queue.dequeue()
        assert queue.empty()

        queue.enqueue(3, 'E')
        queue.enqueue(1, 'F')
        queue.dequeue()
        queue.dequeue()
        assert queue.empty()


    def test_dequeing_from_priority_queue_reflects_priority(self): # pylint: disable=R0201
        queue = PriorityQueue()
        queue.enqueue(4, 'D')
        queue.enqueue(5, 'A')
        queue.enqueue(3, 'B')
        queue.enqueue(7, 'C')

        assert 'B' == queue.dequeue()
        assert 'D' == queue.dequeue()

        queue.enqueue(1, 'E')

        assert 'E' == queue.dequeue()
        assert 'A' == queue.dequeue()
        assert 'C' == queue.dequeue()


    def test_dequeing_from_priority_queue_reflects_modification_of_priority(self): # pylint: disable=R0201
        queue = PriorityQueue()
        queue.enqueue(4, 'D')
        queue.enqueue(5, 'A')
        queue.enqueue(3, 'B')
        queue.enqueue(7, 'C')
        queue.enqueue(1, 'D')
        queue.enqueue(2, 'C')

        assert 'D' == queue.dequeue()
        assert 'C' == queue.dequeue()
        assert 'B' == queue.dequeue()
        assert 'A' == queue.dequeue()


    def test_items_with_modified_priority_are_counted_just_once(self): # pylint: disable=R0201
        queue = PriorityQueue()
        queue.enqueue(5, 'A')
        queue.enqueue(4, 'B')
        queue.enqueue(3, 'A')
        queue.enqueue(6, 'B')

        queue.dequeue()
        queue.dequeue()

        assert queue.empty()

    def test_attempt_to_deque_from_virgin_queue_leads_to_error(self): # pylint: disable=R0201
        queue = PriorityQueue()
        with raises(IndexError, match=r'Cannot dequeue from empty queue\.'):
            queue.dequeue()

    def test_attempt_to_deque_from_empty_queue_leads_to_error(self): # pylint: disable=R0201
        queue = PriorityQueue()
        queue.enqueue(5, 'A')
        queue.enqueue(4, 'B')
        queue.dequeue()
        queue.dequeue()

        with raises(IndexError, match=r'Cannot dequeue from empty queue\.'):
            queue.dequeue()

    def test_attempt_to_deque_from_empty_queue_after_reprioritization_leads_to_error(self): # pylint: disable=R0201
        queue = PriorityQueue()
        queue.enqueue(7, 'A')
        queue.enqueue(4, 'B')
        queue.dequeue()
        queue.enqueue(3, 'A')
        queue.dequeue()

        with raises(IndexError, match=r'Cannot dequeue from empty queue\.'):
            queue.dequeue()
