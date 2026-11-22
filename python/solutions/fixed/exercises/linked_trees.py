"""Reference fixes — linked lists and trees."""

from __future__ import annotations

from collections import deque
from typing import Optional

from exercises.support import ListNode, TreeNode


def reverse_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """LC 25 (Hard). Reverse every full group of k nodes, leave the remainder."""
    node = head
    count = 0
    # FIX: count a full group first; a short tail is returned untouched.
    while node is not None and count < k:
        node = node.next
        count += 1
    if count < k:
        return head
    prev = reverse_k_group(node, k)
    current = head
    for _ in range(k):
        assert current is not None
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    return prev


def max_path_sum(root: Optional[TreeNode]) -> int:
    """LC 124 (Hard). Best path sum between any two nodes."""
    best = float("-inf")

    def gain(node: Optional[TreeNode]) -> int:
        nonlocal best
        if node is None:
            return 0
        # FIX: clamp negative branches to 0 instead of being forced to take them.
        left = max(gain(node.left), 0)
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)
        # FIX: a path through the parent can only use one branch.
        return node.val + max(left, right)

    gain(root)
    return int(best)


def serialize(root: Optional[TreeNode]) -> str:
    """LC 297 (Hard). Pre-order with explicit null markers."""
    out: list[str] = []

    def walk(node: Optional[TreeNode]) -> None:
        if node is None:
            # FIX: nulls must be recorded, or the shape cannot be rebuilt.
            out.append("#")
            return
        out.append(str(node.val))
        walk(node.left)
        walk(node.right)

    walk(root)
    return ",".join(out)


def deserialize(data: str) -> Optional[TreeNode]:
    """LC 297 (Hard). Inverse of :func:`serialize`."""
    tokens = iter(data.split(","))

    def build() -> Optional[TreeNode]:
        token = next(tokens)
        if token == "#":
            return None
        node = TreeNode(int(token))
        node.left = build()
        node.right = build()
        return node

    return build()


def vertical_order(root: Optional[TreeNode]) -> list[list[int]]:
    """LC 987 (Hard). Columns left to right; ties by row, then by value."""
    if root is None:
        return []
    nodes: list[tuple[int, int, int]] = []
    queue: deque[tuple[TreeNode, int, int]] = deque([(root, 0, 0)])
    while queue:
        node, row, col = queue.popleft()
        nodes.append((col, row, node.val))
        if node.left is not None:
            queue.append((node.left, row + 1, col - 1))
        if node.right is not None:
            queue.append((node.right, row + 1, col + 1))
    # FIX: sort by (col, row, value) - BFS order alone is not the required order.
    nodes.sort()
    out: list[list[int]] = []
    last_col: Optional[int] = None
    for col, _row, value in nodes:
        if col != last_col:
            out.append([])
            last_col = col
        out[-1].append(value)
    return out


def longest_increasing_path(matrix: list[list[int]]) -> int:
    """LC 329 (Hard). Longest strictly increasing path in a grid."""
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    cache: dict[tuple[int, int], int] = {}

    def walk(r: int, c: int) -> int:
        # FIX: memoise, otherwise this is exponential.
        if (r, c) in cache:
            return cache[(r, c)]
        best = 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            # FIX: strictly greater; >= would let a flat run repeat forever.
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + walk(nr, nc))
        cache[(r, c)] = best
        return best

    return max(walk(r, c) for r in range(rows) for c in range(cols))
