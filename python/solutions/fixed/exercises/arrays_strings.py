"""Reference fixes — arrays and strings. See solutions/ANSWERS.md."""

from __future__ import annotations

from math import gcd


def first_missing_positive(nums: list[int]) -> int:
    """LC 41 (Hard). Smallest positive integer absent from nums."""
    nums = list(nums)
    n = len(nums)
    for i in range(n):
        # FIX: while, not if - one swap can drop another misplaced value into i.
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1


def trap(height: list[int]) -> int:
    """LC 42 (Hard). Units of rain water trapped."""
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    total = 0
    while left < right:
        # FIX: advance the smaller side, and update the running max before adding.
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            total += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            total += right_max - height[right]
    return total


def candy(ratings: list[int]) -> int:
    """LC 135 (Hard). Minimum candies with the neighbour rule."""
    n = len(ratings)
    if n == 0:
        return 0
    candies = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    # FIX: the right-to-left pass must take the max, not overwrite the left pass.
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
    return sum(candies)


def max_points(points: list[list[int]]) -> int:
    """LC 149 (Hard). Most points on a single straight line."""
    n = len(points)
    if n <= 2:
        return n
    best = 0
    for i in range(n):
        slopes: dict[tuple[int, int], int] = {}
        for j in range(n):
            if i == j:
                continue
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]
            # FIX: reduce by gcd and normalise the sign, so 1/2 and -1/-2 agree.
            divisor = gcd(abs(dx), abs(dy)) or 1
            key = (dx // divisor, dy // divisor)
            if key[0] < 0 or (key[0] == 0 and key[1] < 0):
                key = (-key[0], -key[1])
            slopes[key] = slopes.get(key, 0) + 1
        best = max(best, max(slopes.values()) + 1)
    return best


def full_justify(words: list[str], max_width: int) -> list[str]:
    """LC 68 (Hard). Greedy full text justification."""
    lines: list[str] = []
    line: list[str] = []
    length = 0
    for word in words:
        # FIX: the gap count is len(line), not len(line) - 1, when testing the fit.
        if length + len(line) + len(word) > max_width:
            lines.append(_justify(line, length, max_width))
            line, length = [], 0
        line.append(word)
        length += len(word)
    # FIX: the final line is left-justified and padded, never spread out.
    lines.append(" ".join(line).ljust(max_width))
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
