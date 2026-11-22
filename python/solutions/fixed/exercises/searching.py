"""Reference fixes — binary search on answers and order statistics."""

from __future__ import annotations

from bisect import bisect_left, insort


def find_median_sorted_arrays(a: list[int], b: list[int]) -> float:
    """LC 4 (Hard). Median of two sorted arrays in O(log min(m, n))."""
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    half = (m + n + 1) // 2
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2
        j = half - i
        a_left = a[i - 1] if i > 0 else float("-inf")
        a_right = a[i] if i < m else float("inf")
        b_left = b[j - 1] if j > 0 else float("-inf")
        b_right = b[j] if j < n else float("inf")
        if a_left <= b_right and b_left <= a_right:
            if (m + n) % 2:
                return float(max(a_left, b_left))
            return (max(a_left, b_left) + min(a_right, b_right)) / 2
        # FIX: move the partition in the right direction, and search on the
        # shorter array so j can never fall outside b.
        if a_left > b_right:
            hi = i - 1
        else:
            lo = i + 1
    return 0.0


def split_array(nums: list[int], k: int) -> int:
    """LC 410 (Hard). Minimise the largest subarray sum over k splits."""

    def feasible(cap: int) -> bool:
        parts, current = 1, 0
        for value in nums:
            if current + value > cap:
                parts += 1
                current = value
            else:
                current += value
        return parts <= k

    # FIX: the lower bound is max(nums) - no part can be smaller than its largest element.
    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def smallest_distance_pair(nums: list[int], k: int) -> int:
    """LC 719 (Hard). k-th smallest absolute difference between any two elements."""
    ordered = sorted(nums)

    def count_within(distance: int) -> int:
        total = 0
        left = 0
        for right in range(len(ordered)):
            while ordered[right] - ordered[left] > distance:
                left += 1
            total += right - left
        return total

    lo, hi = 0, ordered[-1] - ordered[0]
    while lo < hi:
        mid = (lo + hi) // 2
        # FIX: >= k, not > k; the k-th value itself must keep the upper half.
        if count_within(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def count_smaller(nums: list[int]) -> list[int]:
    """LC 315 (Hard). For each index, how many later elements are smaller."""
    ordered: list[int] = []
    result: list[int] = []
    # FIX: scan right to left, so "later" really means later.
    for value in reversed(nums):
        result.append(bisect_left(ordered, value))
        insort(ordered, value)
    result.reverse()
    return result
