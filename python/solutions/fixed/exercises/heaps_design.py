"""Reference fixes — heaps and design problems."""

from __future__ import annotations

import heapq
from collections import OrderedDict, defaultdict
from typing import Optional

from exercises.support import ListNode


def merge_k_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    """LC 23 (Hard). Merge k sorted linked lists."""
    heap: list[tuple[int, int, ListNode]] = []
    for i, node in enumerate(lists):
        if node is not None:
            # FIX: the index breaks ties, so heapq never compares two ListNodes.
            heapq.heappush(heap, (node.val, i, node))
    dummy = ListNode()
    tail = dummy
    while heap:
        _, i, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next is not None:
            heapq.heappush(heap, (node.next.val, i, node.next))
    # FIX: cut the tail loose, or the result keeps a stale next pointer.
    tail.next = None
    return dummy.next


class MedianFinder:
    """LC 295 (Hard). Running median over a stream."""

    def __init__(self) -> None:
        self.small: list[int] = []  # max-heap, values negated
        self.large: list[int] = []  # min-heap

    def add_num(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        # FIX: push through the other heap, then rebalance, so every value in
        # `small` really is <= every value in `large`.
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2


def smallest_range(lists: list[list[int]]) -> list[int]:
    """LC 632 (Hard). Smallest range covering at least one number from each list."""
    heap = [(values[0], i, 0) for i, values in enumerate(lists)]
    heapq.heapify(heap)
    right = max(values[0] for values in lists)
    best = [heap[0][0], right]
    while heap:
        value, i, j = heapq.heappop(heap)
        if right - value < best[1] - best[0]:
            best = [value, right]
        # FIX: stop as soon as one list is exhausted - after that no range can
        # cover every list.
        if j + 1 == len(lists[i]):
            break
        nxt = lists[i][j + 1]
        right = max(right, nxt)
        heapq.heappush(heap, (nxt, i, j + 1))
    return best


class LFUCache:
    """LC 460 (Hard). Least-frequently-used cache, LRU as the tie-break."""

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
            # FIX: the minimum only moves up when its bucket empties.
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
            # FIX: overwriting an existing key is a use too.
            self._touch(key)
            return
        if len(self.values) >= self.capacity:
            # FIX: evict from the front of the least-frequent bucket (oldest),
            # not the back.
            old, _ = self.buckets[self.min_count].popitem(last=False)
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
    """LC 502 (Hard). At most k projects, each needing capital you already hold."""
    projects = sorted(zip(capital, profits))
    heap: list[int] = []
    i = 0
    for _ in range(k):
        # FIX: unlock every affordable project before choosing, and choose the
        # most profitable of them.
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(heap, -projects[i][1])
            i += 1
        if not heap:
            break
        w += -heapq.heappop(heap)
    return w
