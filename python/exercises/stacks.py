"""Monotonic stacks and expression parsing."""

from __future__ import annotations


def largest_rectangle_area(heights: list[int]) -> int:
    """LC 84 (Hard). Area of the largest rectangle fitting under the histogram."""
    stack: list[tuple[int, int]] = []  # (start index, height)
    best = 0
    for i, height in enumerate(heights):
        start = i
        while stack and stack[-1][1] >= height:
            index, popped = stack.pop()
            best = max(best, popped * (i - index))
            start = index
        stack.append((start, height))
    return best


def maximal_rectangle(matrix: list[list[str]]) -> int:
    """LC 85 (Hard). Area of the largest rectangle of "1"s in a binary matrix.

    Treats each row as the base of a histogram of consecutive ones above it.
    """
    if not matrix or not matrix[0]:
        return 0
    heights = [0] * len(matrix[0])
    best = 0
    for row in matrix:
        for j, cell in enumerate(row):
            heights[j] += 1 if cell == "1" else 0
        best = max(best, largest_rectangle_area(heights))
    return best


def calculate(s: str) -> int:
    """LC 224 (Hard). Evaluate an expression of non-negative integers, ``+``,
    ``-`` and parentheses. Spaces are ignored. Numbers may have several digits.
    """
    total = 0
    sign = 1
    num = 0
    stack: list[int] = []
    for char in s:
        if char.isdigit():
            num = int(char)
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
    """LC 32 (Hard). Length of the longest *contiguous* well-formed substring.

    Matches each ``)`` against the most recent unmatched ``(``.
    """
    stack: list[str] = []
    pairs = 0
    for char in s:
        if char == "(":
            stack.append(char)
        elif stack:
            stack.pop()
            pairs += 1
    return pairs * 2
