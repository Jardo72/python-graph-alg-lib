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

"""This module some helper functionalities which support the implementation
of the graph algorithms provided by this library.
"""
from abc import ABC
from dataclasses import dataclass, field
from heapq import heappop, heappush
from typing import Any, Dict


@dataclass(frozen=True)
class QueueableItem:
    """Immutable structure carrying a single item that can be enqueued to an
    instance of the :class: RepriorizablePriorityQueue class.

    This structure is part of the public API of the :class: RepriorizablePriorityQueue,
    and it is comprised of the following fields:
    * Unique key of the value carried by this queueable item.
    * Priority of the value carried by this queueable item.
    * Optional data, which is to be used if the item has to carry more than
      just the unique key.
    """
    key: str
    priority: int
    value: Any = None


@dataclass(order=True)
class _QueueEntry:
    """Immutable structure carrying a single element currently being present
    in the priority queue.

    This class is just an internal helper structure, it it not part of the
    public API of the :class: RepriorizablePriorityQueue class.
    """
    priority: int
    item: Any = field(compare=False)
    irrelevant: bool = False


class _AbstractPriorityQueue(ABC): # pylint: disable=R0903
    """Abstract base class providing functionality common to both priority queue
    implementations provided by this module.
    """

    def __init__(self):
        """Constructs a new empty simple priority queue.
        """
        self._heap = []
        self._size = 0


    def is_not_empty(self) -> bool:
        """Verifies whether this queue is not empty.

        Returns:
            bool: True if this queue currrently contains at least one element;
                  False if this queue is currently empty.
        """
        return self._size > 0


class SimplePriorityQueue(_AbstractPriorityQueue):
    """Simple priority queue implementation that does not support modification of
    the priority of the elements currently present in the queue.
    """

    def enqueue(self, priority: int, item: Any):
        """Adds the given item to this queue, using the given priority.

        Args:
            priority (int):     The the priority of the item to be added to
                                this queue.
            item (Any):         The item to be added to this queue.
        """
        queue_entry = _QueueEntry(priority, item)
        heappush(self._heap, queue_entry)
        self._size += 1

    def dequeue(self) -> Any:
        """Dequeues the next item from this queue.

        Raises:
            IndexError: If this queue is empty.

        Returns:
            QueueableItem: The dequeued item.
        """
        if self._size == 0:
            message = 'Cannot dequeue from empty queue.'
            raise IndexError(message)
        entry = heappop(self._heap)
        self._size -= 1
        return entry.item


class RepriorizablePriorityQueue(_AbstractPriorityQueue):
    """Priority queue implementation allowing to modify the priority of
    elements present in the queue.
    """

    def __init__(self):
        """Constructs a new empty repriorizable priority queue.
        """
        super().__init__()
        self._sequence = 0
        self._item_map: Dict[Any, _QueueEntry] = {}

    def enqueue(self, item: QueueableItem):
        """Adds the given item to this queue, using the given priority.

        If an item with the same unique key is already present in this queue,
        and its original priority is distinct from the currently specified
        priority, the new priority is applied. In other words, this method can
        also be used to modify the priority of an item already present in the
        queue. The queue instantly takes the modified priority into account.

        Args:
            item (QueueableItem): The item to be added to this queue.
        """
        queue_entry = _QueueEntry(item.priority, item)
        heappush(self._heap, queue_entry)
        if item.key in self._item_map:
            self._item_map[item.key].irrelevant = True
        else:
            self._size += 1
        self._item_map[item.key] = queue_entry

    def dequeue(self) -> QueueableItem:
        """Dequeues the next item from this queue.

        Raises:
            IndexError: If this queue is empty.

        Returns:
            QueueableItem: The dequeued item.
        """
        while len(self._heap) > 0:
            queue_entry = heappop(self._heap)
            if queue_entry.irrelevant:
                continue
            self._item_map.pop(queue_entry.item.key)
            self._size -= 1
            return queue_entry.item
        message = 'Cannot dequeue from empty queue.'
        raise IndexError(message)


class UnionFind:
    """Implementation of union-find (aka disjoint-set) data structure with path compression.
    """

    def __init__(self, size: int):
        """Constructs a new instance of union-find with the given capacity.

        Args:
            size (int): The number of elements the constructed instance has to support.
        """
        self._element_count = self._subset_count = size
        self._element_parents = []
        self._subset_sizes = []
        for i in range(size):
            self._element_parents.append(i)
            self._subset_sizes.append(1)

    @property
    def element_count(self) -> int:
        """Provides the number of elements present in this union-find instance.
        """
        return self._element_count

    @property
    def subset_count(self) -> int:
        """Provides the number of subsets currently present in this union-find
        instance.
        """
        return self._subset_count

    def find_subset(self, element: int) -> int:
        """Finds and returns the subset the given element currently belongs to.

        Args:
            element (int): The element whose subset is to be found.

        Returns:
            int: The root element of the subset the given element currently belongs to.
        """
        if self._element_parents[element] == element:
            return element

        parent_element = self._element_parents[element]
        while self._element_parents[parent_element] != parent_element:
            parent_element = self._element_parents[parent_element]

        # path compression - set the root element of the subset as parent for all
        # members of the subset, thus eliminating longer chaining of elements
        root_element = parent_element
        parent_element = self._element_parents[element]
        self._element_parents[element] = root_element
        while self._element_parents[parent_element] != parent_element:
            parent_element = self._element_parents[parent_element]
            self._element_parents[parent_element] = root_element

        return root_element

    def subset_size(self, element: int) -> int:
        """Returns the current size of the subset the given element currently belongs
        to.

        Args:
            element (int): The element for which the current size of its subset is to
                           be returned.

        Returns:
            int: The current size of the subset the given element currently belongs to.
        """
        subset = self.find_subset(element)
        return self._subset_sizes[subset]

    def union(self, element_one: int, element_two: int) -> bool:
        """Performs the union of the two subsets the given elements currently belong to.

        This method does nothing if the given elements already belong to the same subset.

        Args:
            element_one (int): The first of the two elements for which the union is to be
                               performed.
            element_two (int): The second of the two elements for which the union is to be
                               performed.

        Returns:
            bool: True if the union operation has been performed; False if the two elements
                  already belong to the same subset, so the union operation is not needed.
        """
        subset_one = self.find_subset(element_one)
        subset_two = self.find_subset(element_two)
        if subset_one == subset_two:
            return False

        if self._subset_sizes[subset_one] < self._subset_sizes[subset_two]:
            self._subset_sizes[subset_two] += self._subset_sizes[subset_one]
            self._element_parents[subset_one] = subset_two
        else:
            self._subset_sizes[subset_one] += self._subset_sizes[subset_two]
            self._element_parents[subset_two] = subset_one
        self._subset_count -= 1
        return True
