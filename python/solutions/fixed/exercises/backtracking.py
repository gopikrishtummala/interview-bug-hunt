"""Reference fixes — backtracking."""

from __future__ import annotations


def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    """LC 212 (Hard). Every dictionary word findable in the grid."""
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
            # FIX: a hit does not end the search - longer words may continue.
            found.add(nxt["$"])
        board[r][c] = "#"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                walk(nr, nc, nxt)
        # FIX: restore the cell on the way out, or later starts see a holed board.
        board[r][c] = char

    for r in range(rows):
        for c in range(cols):
            walk(r, c, trie)
    return sorted(found)


def solve_n_queens(n: int) -> list[list[str]]:
    """LC 51 (Hard). Every distinct n-queens placement."""
    cols: set[int] = set()
    diagonals: set[int] = set()
    anti_diagonals: set[int] = set()
    board: list[list[str]] = []
    out: list[list[str]] = []

    def place(row: int) -> None:
        if row == n:
            out.append(["".join(line) for line in board])
            return
        for col in range(n):
            # FIX: both diagonals are constrained - row-col AND row+col.
            if col in cols or (row - col) in diagonals or (row + col) in anti_diagonals:
                continue
            cols.add(col)
            diagonals.add(row - col)
            anti_diagonals.add(row + col)
            board.append(["."] * n)
            board[-1][col] = "Q"
            place(row + 1)
            # FIX: undo every part of the move, including the board row.
            board.pop()
            cols.remove(col)
            diagonals.remove(row - col)
            anti_diagonals.remove(row + col)

    place(0)
    return out
