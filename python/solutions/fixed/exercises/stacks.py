"""Reference fixes — monotonic stacks and parsing. See solutions/ANSWERS.md."""

from __future__ import annotations


def largest_rectangle_area(heights: list[int]) -> int:
    """LC 84 (Hard). Largest rectangle in a histogram."""
    stack: list[tuple[int, int]] = []  # (start index, height)
    best = 0
    # FIX: the sentinel 0 flushes the stack, so bars still open at the end count.
    for i, height in enumerate(list(heights) + [0]):
        start = i
        while stack and stack[-1][1] >= height:
            index, popped = stack.pop()
            best = max(best, popped * (i - index))
            start = index
        stack.append((start, height))
    return best


def maximal_rectangle(matrix: list[list[str]]) -> int:
    """LC 85 (Hard). Largest all-ones rectangle in a binary matrix."""
    if not matrix or not matrix[0]:
        return 0
    heights = [0] * len(matrix[0])
    best = 0
    for row in matrix:
        for j, cell in enumerate(row):
            # FIX: a zero resets the column height; it does not merely stop growing.
            heights[j] = heights[j] + 1 if cell == "1" else 0
        best = max(best, largest_rectangle_area(heights))
    return best


def calculate(s: str) -> int:
    """LC 224 (Hard). Basic calculator: +, -, parentheses, multi-digit numbers."""
    total = 0
    sign = 1
    num = 0
    stack: list[int] = []
    for char in s:
        if char.isdigit():
            # FIX: accumulate digits, so "42" is forty-two and not four then two.
            num = num * 10 + int(char)
        elif char in "+-":
            total += sign * num
            num = 0
            sign = 1 if char == "+" else -1
        elif char == "(":
            stack.append(total)
            stack.append(sign)
            total = 0
            sign = 1
        elif char == ")":
            total += sign * num
            num = 0
            total *= stack.pop()
            total += stack.pop()
            sign = 1
    return total + sign * num


def longest_valid_parentheses(s: str) -> int:
    """LC 32 (Hard). Longest well-formed substring of parentheses."""
    # FIX: seed with -1 so the first valid run measures from the right base.
    stack = [-1]
    best = 0
    for i, char in enumerate(s):
        if char == "(":
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                best = max(best, i - stack[-1])
    return best
