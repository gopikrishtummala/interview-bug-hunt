"""Heaps and design problems."""

from __future__ import annotations

import heapq
from collections import OrderedDict, defaultdict
from typing import Optional

from exercises.support import ListNode


def merge_k_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    """LC 23 (Hard). Merge ``k`` sorted linked lists into one sorted list."""
    heap: list[tuple[int, ListNode]] = []
    for node in lists:
        if node is not None:
            heapq.heappush(heap, (node.val, node))
    dummy = ListNode()
    tail = dummy
    while heap:
        _, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next is not None:
            heapq.heappush(heap, (node.next.val, node.next))
    return dummy.next


class MedianFinder:
    """LC 295 (Hard). Median of the values seen so far.

    Keeps the low half in a max-heap and the high half in a min-heap, so the
    median is always at one or both tops.
    """

    def __init__(self) -> None:
        self.small: list[int] = []  # max-heap, values negated
        self.large: list[int] = []  # min-heap

    def add_num(self, num: int) -> None:
        if len(self.small) <= len(self.large):
            heapq.heappush(self.small, -num)
        else:
            heapq.heappush(self.large, num)

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2


def smallest_range(lists: list[list[int]]) -> list[int]:
    """LC 632 (Hard). The smallest range ``[lo, hi]`` that includes at least one
    number from each of the ``k`` sorted lists. Ties go to the earliest range.
    """
    heap = [(values[0], i, 0) for i, values in enumerate(lists)]
    heapq.heapify(heap)
    right = max(values[0] for values in lists)
    best = [heap[0][0], right]
    while heap:
        value, i, j = heapq.heappop(heap)
        if right - value <= best[1] - best[0]:
            best = [value, right]
        if j + 1 == len(lists[i]):
            break
        nxt = lists[i][j + 1]
        right = max(right, nxt)
        heapq.heappush(heap, (nxt, i, j + 1))
    return best


class LFUCache:
    """LC 460 (Hard). Evicts the least-frequently-used key; between keys of
    equal frequency, the least recently used one goes. ``get`` returns -1 for a
    missing key. Reading or writing a key counts as a use.
    """

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.values: dict[int, int] = {}
        self.counts: dict[int, int] = {}
        self.buckets: dict[int, OrderedDict[int, None]] = defaultdict(OrderedDict)
        self.min_count = 0

    def _touch(self, key: int) -> None:
        count = self.counts[key]
        del self.buckets[count][key]
        if not self.buckets[count]:
            del self.buckets[count]
            if self.min_count == count:
                self.min_count = count + 1
        self.counts[key] = count + 1
        self.buckets[count + 1][key] = None

    def get(self, key: int) -> int:
        if key not in self.values:
            return -1
        self._touch(key)
        return self.values[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.values:
            self.values[key] = value
            return
        if len(self.values) >= self.capacity:
            old, _ = self.buckets[self.min_count].popitem(last=True)
            if not self.buckets[self.min_count]:
                del self.buckets[self.min_count]
            del self.values[old]
            del self.counts[old]
        self.values[key] = value
        self.counts[key] = 1
        self.buckets[1][key] = None
        self.min_count = 1


def find_maximized_capital(
    k: int, w: int, profits: list[int], capital: list[int]
) -> int:
    """LC 502 (Hard). Pick at most ``k`` projects, each needing capital you
    already hold, to maximise final capital. Profits are added to capital.
    """
    projects = sorted(zip(capital, profits))
    heap: list[int] = []
    i = 0
    for _ in range(k):
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(heap, projects[i][1])
            i += 1
        if not heap:
            break
        w += heapq.heappop(heap)
    return w
