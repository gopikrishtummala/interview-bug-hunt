"""Greedy and interval scheduling."""

from __future__ import annotations

import heapq
from bisect import bisect_left


def job_scheduling(
    start_time: list[int], end_time: list[int], profit: list[int]
) -> int:
    """LC 1235 (Hard). Maximum profit from a subset of non-overlapping jobs.

    A job starting exactly when another ends does not overlap it.
    """
    jobs = sorted(zip(end_time, start_time, profit))
    ends = [0]
    best = [0]
    for end, start, value in jobs:
        i = bisect_left(ends, start) - 1
        candidate = best[i] + value
        if candidate > best[-1]:
            ends.append(end)
            best.append(candidate)
    return best[-1]


def min_interval(intervals: list[list[int]], queries: list[int]) -> list[int]:
    """LC 1851 (Hard). For each query, the size of the smallest interval
    ``[l, r]`` with ``l <= query <= r``, where size is ``r - l + 1``; -1 when no
    interval covers it. Answers come back in the order the queries were given.
    """
    ordered = sorted(intervals)
    answer: dict[int, int] = {}
    heap: list[tuple[int, int]] = []
    i = 0
    for query in queries:
        while i < len(ordered) and ordered[i][0] <= query:
            left, right = ordered[i]
            heapq.heappush(heap, (right - left + 1, right))
            i += 1
        while heap and heap[0][1] < query:
            heapq.heappop(heap)
        answer[query] = heap[0][0] if heap else -1
    return [answer[query] for query in queries]


def employee_free_time(schedule: list[list[list[int]]]) -> list[list[int]]:
    """LC 759 (Hard). The finite intervals during which *every* employee is
    free, in ascending order. Each employee's own intervals are sorted and
    disjoint, but different employees overlap freely.
    """
    intervals = sorted(
        (start, end) for person in schedule for start, end in person
    )
    if not intervals:
        return []
    free: list[list[int]] = []
    _, end = intervals[0]
    for start, finish in intervals[1:]:
        if start > end:
            free.append([end, start])
        end = finish
    return free
