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
from dataclasses import dataclass, field
from heapq import heappop, heappush
from typing import Any, Dict


@dataclass(frozen=True)
class QueueableItem:
    """Immutable structure carrying a single item that can be enqueued to an
    instance of the :class: PriorityQueue class.

    This structure is part of the public API of the :class: PriorityQueue,
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
    public API of the :class: PriorityQueue class.
    """
    priority: int
    item: Any = field(compare=False)
    irrelevant: bool = False


class PriorityQueue:
    """Priority queue implementation allowing to modify the priority of
    elements present in the queue.
    """

    def __init__(self):
        """Constructs a new empty priority queue.
        """
        self._sequence = 0
        self._heap = []
        self._size = 0
        self._item_map: Dict[Any, _QueueEntry] = {}

    def empty(self) -> bool:
        """Verifies whether this queue is empty.

        Returns:
            bool: True if this queue currrently does not contain any element;
                  False otherwise.
        """
        return self._size == 0

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
