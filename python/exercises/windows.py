"""Sliding window and two pointers."""

from __future__ import annotations

from collections import Counter, deque


def min_window(s: str, t: str) -> str:
    """LC 76 (Hard). The shortest substring of ``s`` containing every character
    of ``t``, counting duplicates. Empty string when there is none.
    """
    if not s or not t:
        return ""
    need = Counter(t)
    missing = len(t)
    left = start = end = 0
    for right, char in enumerate(s, 1):
        if need[char] > 0:
            missing -= 1
        need[char] -= 1
        if missing == 0:
            while need[s[left]] < 0:
                need[s[left]] += 1
                left += 1
            if end == 0:
                start, end = left, right
            need[s[left]] += 1
            missing += 1
            left += 1
    return s[start:end]


def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """LC 239 (Hard). The maximum of each window of size ``k``, left to right.

    Keeps a deque of indices whose values are strictly decreasing, so the front
    is always the maximum of the current window.
    """
    queue: deque[int] = deque()
    out: list[int] = []
    for i, value in enumerate(nums):
        while queue and nums[queue[-1]] <= value:
            queue.pop()
        queue.append(i)
        if i >= k - 1:
            out.append(nums[queue[0]])
    return out


def find_substring(s: str, words: list[str]) -> list[int]:
    """LC 30 (Hard). Every start index of a substring that is a concatenation of
    all of ``words``, each used exactly once, in any order.
    """
    if not s or not words:
        return []
    width = len(words[0])
    need = Counter(words)
    result: list[int] = []
    left = 0
    count = 0
    window: Counter[str] = Counter()
    for right in range(0, len(s) - width + 1, width):
        word = s[right : right + width]
        if word in need:
            window[word] += 1
            count += 1
            while window[word] > need[word]:
                window[s[left : left + width]] -= 1
                left += width
                count -= 1
            if count == len(words):
                result.append(left)
                window[s[left : left + width]] -= 1
                left += width
                count -= 1
        else:
            window.clear()
            count = 0
            left = right + width
    return sorted(result)


def shortest_subarray(nums: list[int], k: int) -> int:
    """LC 862 (Hard). Length of the shortest non-empty subarray whose sum is at
    least ``k``, or -1 if there is none. ``nums`` may contain negatives.
    """
    n = len(nums)
    prefix = [0] * (n + 1)
    for i, value in enumerate(nums):
        prefix[i + 1] = prefix[i] + value
    best = n + 1
    queue: deque[int] = deque()
    for i, total in enumerate(prefix):
        while queue and total - prefix[queue[0]] > k:
            best = min(best, i - queue.popleft())
        while queue and prefix[queue[-1]] >= total:
            queue.pop()
        queue.append(i)
    return best if best <= n else -1


def subarrays_with_k_distinct(nums: list[int], k: int) -> int:
    """LC 992 (Hard). Number of subarrays containing exactly ``k`` distinct
    values.
    """
    return _at_most(nums, k)


def _at_most(nums: list[int], k: int) -> int:
    if k <= 0:
        return 0
    count: Counter[int] = Counter()
    total = 0
    left = 0
    for right, value in enumerate(nums):
        count[value] += 1
        while len(count) > k:
            count[nums[left]] -= 1
            if count[nums[left]] == 0:
                del count[nums[left]]
            left += 1
        total += right - left + 1
    return total
