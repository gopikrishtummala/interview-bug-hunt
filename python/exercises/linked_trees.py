"""Linked lists and trees."""

from __future__ import annotations

from collections import deque
from typing import Optional

from exercises.support import ListNode, TreeNode


def reverse_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """LC 25 (Hard). Reverse the nodes ``k`` at a time.

    If the number of remaining nodes is fewer than ``k``, those nodes are left
    in their original order.
    """
    node = head
    count = 0
    while node is not None and count < k:
        node = node.next
        count += 1
    prev = reverse_k_group(node, k)
    current = head
    for _ in range(count):
        assert current is not None
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    return prev


def max_path_sum(root: Optional[TreeNode]) -> int:
    """LC 124 (Hard). The largest sum along any path between two nodes.

    A path need not pass through the root, and a single node is a valid path.
    """
    best = float("-inf")

    def gain(node: Optional[TreeNode]) -> int:
        nonlocal best
        if node is None:
            return 0
        left = gain(node.left)
        right = gain(node.right)
        best = max(best, node.val + left + right)
        return node.val + left + right

    gain(root)
    return int(best)


def serialize(root: Optional[TreeNode]) -> str:
    """LC 297 (Hard). Encode a tree as a comma-separated pre-order string.

    ``deserialize(serialize(root))`` must rebuild the identical tree.
    """
    out: list[str] = []

    def walk(node: Optional[TreeNode]) -> None:
        if node is None:
            return
        out.append(str(node.val))
        walk(node.left)
        walk(node.right)

    walk(root)
    return ",".join(out)


def deserialize(data: str) -> Optional[TreeNode]:
    """LC 297 (Hard). Rebuild the tree encoded by :func:`serialize`."""
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
    """LC 987 (Hard). Vertical order traversal.

    Columns are reported left to right. Within a column, nodes are ordered by
    row; two nodes in the same row and column are ordered by value.
    """
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
    out: list[list[int]] = []
    last_col: Optional[int] = None
    for col, _row, value in nodes:
        if col != last_col:
            out.append([])
            last_col = col
        out[-1].append(value)
    return out


def longest_increasing_path(matrix: list[list[int]]) -> int:
    """LC 329 (Hard). Length of the longest strictly increasing path, moving
    only up, down, left or right.
    """
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])

    def walk(r: int, c: int) -> int:
        best = 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] >= matrix[r][c]:
                best = max(best, 1 + walk(nr, nc))
        return best

    return max(walk(r, c) for r in range(rows) for c in range(cols))
