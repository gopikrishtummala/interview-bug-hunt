"""Dynamic programming."""

from __future__ import annotations

from bisect import bisect_left


def min_distance(word1: str, word2: str) -> int:
    """LC 72 (Hard). Minimum number of single-character insertions, deletions or
    substitutions that turn ``word1`` into ``word2``.
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


def num_distinct(s: str, t: str) -> int:
    """LC 115 (Hard). Number of distinct subsequences of ``s`` equal to ``t``."""
    dp = [0] * (len(t) + 1)
    dp[0] = 1
    for char in s:
        for j in range(1, len(t) + 1):
            if t[j - 1] == char:
                dp[j] += dp[j - 1]
    return dp[len(t)]


def max_coins(nums: list[int]) -> int:
    """LC 312 (Hard). Maximum coins from bursting all the balloons, where
    bursting balloon ``i`` pays ``left * i * right`` for its current neighbours
    and the array then closes up. Out-of-range neighbours count as 1.
    """
    values = [1] + list(nums) + [1]
    n = len(values)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for left in range(0, n - length):
            right = left + length
            for k in range(left + 1, right):
                dp[left][right] = max(
                    dp[left][right],
                    values[k - 1] * values[k] * values[k + 1]
                    + dp[left][k]
                    + dp[k][right],
                )
    return dp[0][n - 1]


def is_match_regex(s: str, p: str) -> bool:
    """LC 10 (Hard). Full regular expression match where ``.`` matches any
    single character and ``*`` matches zero or more of *the element before it*.
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(1, n + 1):
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 1]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == "*":
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
            else:
                dp[i][j] = dp[i - 1][j - 1] and p[j - 1] in (".", s[i - 1])
    return dp[m][n]


def is_match_wildcard(s: str, p: str) -> bool:
    """LC 44 (Hard). Wildcard match where ``?`` matches any single character and
    ``*`` matches any sequence, including the empty one.
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(1, n + 1):
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 1]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == "*":
                dp[i][j] = dp[i][j - 1]
            else:
                dp[i][j] = dp[i - 1][j - 1] and p[j - 1] in ("?", s[i - 1])
    return dp[m][n]


def is_interleave(s1: str, s2: str, s3: str) -> bool:
    """LC 97 (Hard). True when ``s3`` is formed by interleaving ``s1`` and
    ``s2``, keeping the relative order of each.
    """
    dp = [[False] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    dp[0][0] = True
    for i in range(len(s1) + 1):
        for j in range(len(s2) + 1):
            if i > 0 and s1[i - 1] == s3[i + j - 1] and dp[i - 1][j]:
                dp[i][j] = True
            if j > 0 and s2[j - 1] == s3[i + j - 1] and dp[i][j - 1]:
                dp[i][j] = True
    return dp[len(s1)][len(s2)]


def min_cut(s: str) -> int:
    """LC 132 (Hard). Minimum cuts so that every resulting piece is a
    palindrome.
    """
    n = len(s)
    if n <= 1:
        return 0
    is_pal = [[False] * n for _ in range(n)]
    cuts = [0] * n
    for end in range(n):
        best = end
        for start in range(end + 1):
            if s[start] == s[end] and (end - start < 2 or is_pal[start + 1][end - 1]):
                is_pal[start][end] = True
                best = min(best, cuts[start - 1] + 1)
        cuts[end] = best
    return cuts[n - 1]


def max_envelopes(envelopes: list[list[int]]) -> int:
    """LC 354 (Hard). Most envelopes that can be nested, where one fits inside
    another only if both its width and its height are strictly smaller.
    """
    ordered = sorted(envelopes, key=lambda e: (e[0], e[1]))
    tails: list[int] = []
    for _width, height in ordered:
        i = bisect_left(tails, height)
        if i == len(tails):
            tails.append(height)
        else:
            tails[i] = height
    return len(tails)


def word_break_ii(s: str, word_dict: list[str]) -> list[str]:
    """LC 140 (Hard). Every sentence, words separated by single spaces, that can
    be formed from ``s`` using the dictionary. Returned in sorted order.
    """
    words = set(word_dict)
    memo: dict[int, list[str]] = {}

    def build(start: int) -> list[str]:
        if start == len(s):
            return [""]
        if start in memo:
            return memo[start]
        out: list[str] = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in words:
                for rest in build(end):
                    out.append(word + " " + rest)
        memo[start] = out
        return out

    return sorted(build(0))


def calculate_minimum_hp(dungeon: list[list[int]]) -> int:
    """LC 174 (Hard). The lowest starting health that lets the knight walk from
    the top-left to the bottom-right moving only right or down, with health
    staying strictly positive the whole way.
    """
    rows, cols = len(dungeon), len(dungeon[0])
    inf = float("inf")
    dp = [[inf] * (cols + 1) for _ in range(rows + 1)]
    dp[rows][cols - 1] = 1
    dp[rows - 1][cols] = 1
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            dp[r][c] = min(dp[r + 1][c], dp[r][c + 1]) - dungeon[r][c]
    return int(dp[0][0])
