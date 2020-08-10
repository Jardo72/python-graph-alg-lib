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

from graphlib.util import QueueableItem, RepriorizablePriorityQueue, SimplePriorityQueue


class TestSimplePriorityQueue: # pylint: disable=R0201,C0116
    """Collection of test methods exercising the class :class:
    graphlib.util.SimplePriorityQueue.
    """

    def test_virgin_priority_queue_is_empty(self):
        queue = SimplePriorityQueue()
        assert queue.empty

    def test_priority_queue_with_elements_is_not_empty(self):
        queue = SimplePriorityQueue()

        queue.enqueue(priority=4, item='D')
        assert not queue.empty()

        queue.enqueue(priority=5, item='A')
        assert not queue.empty()

        queue.enqueue(priority=3, item='B', )
        assert not queue.empty()

        queue.dequeue()
        assert not queue.empty()

        queue.dequeue()
        assert not queue.empty()

    def test_priority_queue_after_removal_of_last_element_is_empty(self):
        queue = SimplePriorityQueue()

        queue.enqueue(priority=5, item='A')
        queue.enqueue(priority=3, item='B')
        queue.dequeue()
        queue.enqueue(priority=4, item='C')
        queue.dequeue()
        queue.dequeue()
        assert queue.empty()

        queue.enqueue(priority=2, item='D')
        queue.dequeue()
        assert queue.empty()

        queue.enqueue(priority=3, item='E')
        queue.enqueue(priority=1, item='F')
        queue.dequeue()
        queue.dequeue()
        assert queue.empty()

    def test_dequeing_from_priority_queue_reflects_priority(self):
        queue = SimplePriorityQueue()
        queue.enqueue(priority=4, item='D')
        queue.enqueue(priority=5, item='A')
        queue.enqueue(priority=3, item='B')
        queue.enqueue(priority=7, item='C')

        assert queue.dequeue() == 'B'
        assert queue.dequeue() == 'D'

        queue.enqueue(priority=1, item='E')

        assert queue.dequeue() == 'E'
        assert queue.dequeue() == 'A'
        assert queue.dequeue() == 'C'

    def test_attempt_to_deque_from_virgin_queue_leads_to_error(self):
        queue = SimplePriorityQueue()
        with raises(IndexError, match=r'Cannot dequeue from empty queue\.'):
            queue.dequeue()

    def test_attempt_to_deque_from_empty_queue_leads_to_error(self):
        queue = SimplePriorityQueue()
        queue.enqueue(priority=5, item='A')
        queue.enqueue(priority=4, item='B')
        queue.dequeue()
        queue.dequeue()

        with raises(IndexError, match=r'Cannot dequeue from empty queue\.'):
            queue.dequeue()


class TestRepriorizablePriorityQueue: # pylint: disable=R0201,C0116
    """Collection of test methods exercising the class :class:
    graphlib.util.RepriorizablePriorityQueue.
    """

    def test_virgin_priority_queue_is_empty(self):
        queue = RepriorizablePriorityQueue()
        assert queue.empty

    def test_priority_queue_with_elements_is_not_empty(self):
        queue = RepriorizablePriorityQueue()

        queue.enqueue(QueueableItem('D', 4))
        assert not queue.empty()

        queue.enqueue(QueueableItem('A', 5))
        assert not queue.empty()

        queue.enqueue(QueueableItem('B', 3))
        assert not queue.empty()

        queue.dequeue()
        assert not queue.empty()

        queue.dequeue()
        assert not queue.empty()

    def test_priority_queue_after_removal_of_last_element_is_empty(self):
        queue = RepriorizablePriorityQueue()

        queue.enqueue(QueueableItem('A', 5))
        queue.enqueue(QueueableItem('B', 3))
        queue.dequeue()
        queue.enqueue(QueueableItem('C', 4))
        queue.dequeue()
        queue.dequeue()
        assert queue.empty()

        queue.enqueue(QueueableItem('D', 2))
        queue.dequeue()
        assert queue.empty()

        queue.enqueue(QueueableItem('E', 3))
        queue.enqueue(QueueableItem('F', 1))
        queue.dequeue()
        queue.dequeue()
        assert queue.empty()

    def test_dequeing_from_priority_queue_reflects_priority(self):
        queue = RepriorizablePriorityQueue()
        queue.enqueue(QueueableItem('D', 4))
        queue.enqueue(QueueableItem('A', 5))
        queue.enqueue(QueueableItem('B', 3))
        queue.enqueue(QueueableItem('C', 7))

        assert queue.dequeue() == QueueableItem('B', 3)
        assert queue.dequeue() == QueueableItem('D', 4)

        queue.enqueue(QueueableItem('E', 1))

        assert queue.dequeue() == QueueableItem('E', 1)
        assert queue.dequeue() == QueueableItem('A', 5)
        assert queue.dequeue() == QueueableItem('C', 7)

    def test_dequeing_from_priority_queue_reflects_modification_of_priority(self):
        queue = RepriorizablePriorityQueue()
        queue.enqueue(QueueableItem('D', 4))
        queue.enqueue(QueueableItem('A', 5))
        queue.enqueue(QueueableItem('B', 3))
        queue.enqueue(QueueableItem('C', 7))
        queue.enqueue(QueueableItem('D', 1))
        queue.enqueue(QueueableItem('C', 2))

        assert queue.dequeue() == QueueableItem('D', 1)
        assert queue.dequeue() == QueueableItem('C', 2)
        assert queue.dequeue() == QueueableItem('B', 3)
        assert queue.dequeue() == QueueableItem('A', 5)

    def test_items_with_modified_priority_are_counted_just_once(self):
        queue = RepriorizablePriorityQueue()
        queue.enqueue(QueueableItem('A', 5))
        queue.enqueue(QueueableItem('B', 4))
        queue.enqueue(QueueableItem('A', 3))
        queue.enqueue(QueueableItem('B', 6))

        queue.dequeue()
        queue.dequeue()

        assert queue.empty()

    def test_attempt_to_deque_from_virgin_queue_leads_to_error(self):
        queue = RepriorizablePriorityQueue()
        with raises(IndexError, match=r'Cannot dequeue from empty queue\.'):
            queue.dequeue()

    def test_attempt_to_deque_from_empty_queue_leads_to_error(self):
        queue = RepriorizablePriorityQueue()
        queue.enqueue(QueueableItem('A', 5))
        queue.enqueue(QueueableItem('B', 4))
        queue.dequeue()
        queue.dequeue()

        with raises(IndexError, match=r'Cannot dequeue from empty queue\.'):
            queue.dequeue()

    def test_attempt_to_deque_from_empty_queue_after_reprioritization_leads_to_error(self):
        queue = RepriorizablePriorityQueue()
        queue.enqueue(QueueableItem('A', 7))
        queue.enqueue(QueueableItem('B', 4))
        queue.dequeue()
        queue.enqueue(QueueableItem('A', 3))
        queue.dequeue()

        with raises(IndexError, match=r'Cannot dequeue from empty queue\.'):
            queue.dequeue()
