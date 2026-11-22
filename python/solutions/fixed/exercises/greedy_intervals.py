"""Reference fixes — greedy and interval scheduling."""

from __future__ import annotations

import heapq
from bisect import bisect_right


def job_scheduling(
    start_time: list[int], end_time: list[int], profit: list[int]
) -> int:
    """LC 1235 (Hard). Maximum profit from non-overlapping jobs."""
    # FIX: order by end time, so every earlier job is a candidate predecessor.
    jobs = sorted(zip(end_time, start_time, profit))
    ends = [0]
    best = [0]
    for end, start, value in jobs:
        # FIX: bisect_right - a job starting exactly when another ends is allowed.
        i = bisect_right(ends, start) - 1
        candidate = best[i] + value
        if candidate > best[-1]:
            ends.append(end)
            best.append(candidate)
    return best[-1]


def min_interval(intervals: list[list[int]], queries: list[int]) -> list[int]:
    """LC 1851 (Hard). Size of the smallest interval covering each query."""
    ordered = sorted(intervals)
    answer: dict[int, int] = {}
    heap: list[tuple[int, int]] = []
    i = 0
    # FIX: sort the queries for the sweep, then restore the caller's order.
    for query in sorted(queries):
        while i < len(ordered) and ordered[i][0] <= query:
            left, right = ordered[i]
            heapq.heappush(heap, (right - left + 1, right))
            i += 1
        while heap and heap[0][1] < query:
            heapq.heappop(heap)
        answer[query] = heap[0][0] if heap else -1
    return [answer[query] for query in queries]


def employee_free_time(schedule: list[list[list[int]]]) -> list[list[int]]:
    """LC 759 (Hard). Gaps common to every employee."""
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
        # FIX: the running end is the max so far; a nested interval must not
        # shrink it back.
        end = max(end, finish)
    return free
