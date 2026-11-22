"""Backtracking."""

from __future__ import annotations


def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    """LC 212 (Hard). Every word from ``words`` that can be read off the board by
    walking between side-adjacent cells, using each cell at most once per word.
    Returned in sorted order.
    """
    trie: dict = {}
    for word in words:
        node = trie
        for char in word:
            node = node.setdefault(char, {})
        node["$"] = word

    rows, cols = len(board), len(board[0])
    found: set[str] = set()

    def walk(r: int, c: int, node: dict) -> None:
        char = board[r][c]
        if char not in node:
            return
        nxt = node[char]
        if "$" in nxt:
            found.add(nxt["$"])
        board[r][c] = "#"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                walk(nr, nc, nxt)

    for r in range(rows):
        for c in range(cols):
            walk(r, c, trie)
    return sorted(found)


def solve_n_queens(n: int) -> list[list[str]]:
    """LC 51 (Hard). Every distinct placement of ``n`` queens on an n x n board
    with no two attacking each other. Each board is a list of rows, with 'Q' for
    a queen and '.' for an empty square.
    """
    cols: set[int] = set()
    diagonals: set[int] = set()
    board: list[list[str]] = []
    out: list[list[str]] = []

    def place(row: int) -> None:
        if row == n:
            out.append(["".join(line) for line in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diagonals:
                continue
            cols.add(col)
            diagonals.add(row - col)
            board.append(["."] * n)
            board[-1][col] = "Q"
            place(row + 1)
            board.pop()
            cols.remove(col)
            diagonals.remove(row - col)

    place(0)
    return out
