"""Fixtures shared by the exercises and the spec.

This file is NOT part of the exercise. It is known good — no bugs are planted
here, and you should not need to change it.
"""

from __future__ import annotations

from collections import deque
from typing import Any, Iterable, Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"ListNode({self.val})"


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"TreeNode({self.val})"


def to_linked(values: Iterable[int]) -> Optional[ListNode]:
    head: Optional[ListNode] = None
    for value in reversed(list(values)):
        head = ListNode(value, head)
    return head


def from_linked(node: Optional[ListNode], limit: int = 10_000) -> list[int]:
    out: list[int] = []
    while node is not None and len(out) < limit:
        out.append(node.val)
        node = node.next
    return out


def build_tree(values: list[Any]) -> Optional[TreeNode]:
    """Level-order list with ``None`` holes, LeetCode style."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values):
            value = values[i]
            i += 1
            if value is not None:
                node.left = TreeNode(value)
                queue.append(node.left)
        if i < len(values):
            value = values[i]
            i += 1
            if value is not None:
                node.right = TreeNode(value)
                queue.append(node.right)
    return root


def tree_to_list(root: Optional[TreeNode]) -> list[Any]:
    if root is None:
        return []
    out: list[Any] = []
    queue: deque[Optional[TreeNode]] = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out
