"""Arrays and strings.

Each function's docstring is the spec. The implementations below are complete,
idiomatic and confident. They are also wrong.
"""

from __future__ import annotations


def first_missing_positive(nums: list[int]) -> int:
    """LC 41 (Hard). Smallest positive integer missing from ``nums``.

    Runs in O(n) time and O(1) extra space by placing each value v in slot v-1.
    """
    nums = list(nums)
    n = len(nums)
    for i in range(n):
        if 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1


def trap(height: list[int]) -> int:
    """LC 42 (Hard). Units of rain water trapped between the bars."""
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    total = 0
    while left < right:
        if left_max > right_max:
            left += 1
            left_max = max(left_max, height[left])
            total += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            total += right_max - height[right]
    return total


def candy(ratings: list[int]) -> int:
    """LC 135 (Hard). Fewest candies so every child gets at least one and any
    child rated higher than a neighbour gets more than that neighbour.

    Two passes: left to right for the rising runs, right to left for the falling
    ones.
    """
    n = len(ratings)
    if n == 0:
        return 0
    candies = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = candies[i + 1] + 1
    return sum(candies)


def max_points(points: list[list[int]]) -> int:
    """LC 149 (Hard). Largest number of points lying on one straight line."""
    n = len(points)
    if n <= 2:
        return n
    best = 0
    for i in range(n):
        slopes: dict[float, int] = {}
        for j in range(n):
            if i == j:
                continue
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]
            slope = dy / dx
            slopes[slope] = slopes.get(slope, 0) + 1
        best = max(best, max(slopes.values()) + 1)
    return best


def full_justify(words: list[str], max_width: int) -> list[str]:
    """LC 68 (Hard). Greedy full justification.

    Packs as many words as fit on each line, spreads the spaces as evenly as
    possible with the extra spaces going to the left-hand gaps, and
    left-justifies the final line, padding it to ``max_width``.
    """
    lines: list[str] = []
    line: list[str] = []
    length = 0
    for word in words:
        if length + len(line) - 1 + len(word) > max_width:
            lines.append(_justify(line, length, max_width))
            line, length = [], 0
        line.append(word)
        length += len(word)
    lines.append(_justify(line, length, max_width))
    return lines


def _justify(line: list[str], length: int, max_width: int) -> str:
    if len(line) == 1:
        return line[0].ljust(max_width)
    spaces = max_width - length
    gaps = len(line) - 1
    base, extra = divmod(spaces, gaps)
    out = ""
    for i, token in enumerate(line[:-1]):
        out += token + " " * (base + (1 if i < extra else 0))
    return out + line[-1]
