"""Binary search on the answer, and order statistics."""

from __future__ import annotations

from bisect import bisect_left, insort


def find_median_sorted_arrays(a: list[int], b: list[int]) -> float:
    """LC 4 (Hard). Median of two sorted arrays, in O(log(m + n)).

    Binary searches the partition point so that everything left of the cut is
    <= everything right of it.
    """
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
        if a_left > b_right:
            hi = i - 1
        else:
            lo = i + 1
    return 0.0


def split_array(nums: list[int], k: int) -> int:
    """LC 410 (Hard). Split ``nums`` into ``k`` contiguous subarrays so that the
    largest subarray sum is as small as possible; return that sum.
    """

    def feasible(cap: int) -> bool:
        parts, current = 1, 0
        for value in nums:
            if current + value >= cap:
                parts += 1
                current = value
            else:
                current += value
        return parts <= k

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def smallest_distance_pair(nums: list[int], k: int) -> int:
    """LC 719 (Hard). The k-th smallest absolute difference over all pairs
    (1-indexed).
    """
    ordered = sorted(nums)

    def count_within(distance: int) -> int:
        total = 0
        left = 0
        for right in range(len(ordered)):
            while ordered[right] - ordered[left] > distance:
                left += 1
            total += right - left + 1
        return total

    lo, hi = 0, ordered[-1] - ordered[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_within(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def count_smaller(nums: list[int]) -> list[int]:
    """LC 315 (Hard). ``result[i]`` is the number of elements to the *right* of
    ``i`` that are smaller than ``nums[i]``.
    """
    ordered: list[int] = []
    result: list[int] = []
    for value in nums:
        result.append(bisect_left(ordered, value))
        insort(ordered, value)
    return result
