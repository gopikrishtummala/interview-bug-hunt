"""Reference fixes — sliding window and two pointers. See solutions/ANSWERS.md."""

from __future__ import annotations

from collections import Counter, deque


def min_window(s: str, t: str) -> str:
    """LC 76 (Hard). Smallest window of s containing all of t, multiplicity included."""
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
            # FIX: keep the smallest window, do not return the first one found.
            if end == 0 or right - left < end - start:
                start, end = left, right
            need[s[left]] += 1
            missing += 1
            left += 1
    return s[start:end]


def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """LC 239 (Hard). Maximum of every window of size k."""
    queue: deque[int] = deque()
    out: list[int] = []
    for i, value in enumerate(nums):
        # FIX: pop from the back while the tail is <= the new value.
        while queue and nums[queue[-1]] <= value:
            queue.pop()
        queue.append(i)
        if queue[0] <= i - k:
            queue.popleft()
        if i >= k - 1:
            out.append(nums[queue[0]])
    return out


def find_substring(s: str, words: list[str]) -> list[int]:
    """LC 30 (Hard). Start indices of concatenations of every word, in any order."""
    if not s or not words:
        return []
    width = len(words[0])
    need = Counter(words)
    result: list[int] = []
    # FIX: every alignment must be scanned, not just offset 0.
    for offset in range(width):
        left = offset
        count = 0
        window: Counter[str] = Counter()
        for right in range(offset, len(s) - width + 1, width):
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
    """LC 862 (Hard). Shortest subarray with sum >= k, negatives allowed."""
    n = len(nums)
    prefix = [0] * (n + 1)
    for i, value in enumerate(nums):
        prefix[i + 1] = prefix[i] + value
    best = n + 1
    queue: deque[int] = deque()
    for i, total in enumerate(prefix):
        # FIX: a monotonic deque over prefix sums; a plain window breaks on negatives.
        while queue and total - prefix[queue[0]] >= k:
            best = min(best, i - queue.popleft())
        while queue and prefix[queue[-1]] >= total:
            queue.pop()
        queue.append(i)
    return best if best <= n else -1


def subarrays_with_k_distinct(nums: list[int], k: int) -> int:
    """LC 992 (Hard). Subarrays containing exactly k distinct values."""
    # FIX: exactly k is at-most-k minus at-most-(k-1); one window cannot do it alone.
    return _at_most(nums, k) - _at_most(nums, k - 1)


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
