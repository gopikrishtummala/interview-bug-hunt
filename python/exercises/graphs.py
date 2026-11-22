"""Graphs."""

from __future__ import annotations

import heapq
from collections import defaultdict, deque
from string import ascii_lowercase


def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    """LC 127 (Hard). Number of words in the shortest transformation sequence
    from ``begin_word`` to ``end_word``, counting both ends, changing one letter
    at a time and staying inside ``word_list``. 0 when impossible.
    """
    words = set(word_list)
    if end_word not in words:
        return 0
    queue: deque[tuple[str, int]] = deque([(begin_word, 1)])
    seen = {begin_word}
    while queue:
        word, steps = queue.popleft()
        if word == end_word:
            return steps
        for i in range(len(word)):
            for letter in ascii_lowercase:
                nxt = word[:i] + letter + word[i + 1 :]
                if nxt in words and nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, steps))
    return 0


def alien_order(words: list[str]) -> str:
    """LC 269 (Hard). A letter order consistent with this sorted dictionary, or
    "" when the input is contradictory. Ties are broken lexicographically so the
    result is deterministic.
    """
    adjacency: dict[str, set[str]] = {c: set() for word in words for c in word}
    indegree: dict[str, int] = {c: 0 for c in adjacency}
    for first, second in zip(words, words[1:]):
        for a, b in zip(first, second):
            if a != b:
                if b not in adjacency[a]:
                    adjacency[a].add(b)
                    indegree[b] += 1
                break
    queue = deque(sorted(c for c in indegree if indegree[c] == 0))
    out: list[str] = []
    while queue:
        char = queue.popleft()
        out.append(char)
        for nxt in sorted(adjacency[char]):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return "".join(out) if len(out) == len(adjacency) else ""


def find_itinerary(tickets: list[list[str]]) -> list[str]:
    """LC 332 (Hard). Reconstruct the itinerary that uses every ticket exactly
    once, starting at JFK. When several are possible, return the one that is
    smallest in lexical order.
    """
    graph: dict[str, list[str]] = defaultdict(list)
    for src, dst in sorted(tickets):
        graph[src].append(dst)
    route: list[str] = []

    def visit(airport: str) -> None:
        while graph[airport]:
            visit(graph[airport].pop())
        route.append(airport)

    visit("JFK")
    return route[::-1]


def swim_in_water(grid: list[list[int]]) -> int:
    """LC 778 (Hard). The least time t at which you can walk from (0, 0) to the
    bottom-right corner, where a cell is passable once t >= its height.
    """
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]
    seen = {(0, 0)}
    time = 0
    while heap:
        height, r, c = heapq.heappop(heap)
        time += height
        if r == n - 1 and c == n - 1:
            return time
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
                seen.add((nr, nc))
                heapq.heappush(heap, (grid[nr][nc], nr, nc))
    return -1


def critical_connections(n: int, connections: list[list[int]]) -> list[list[int]]:
    """LC 1192 (Hard). All critical connections: edges whose removal would
    disconnect the network. Each edge is returned sorted, and the list is
    sorted too.
    """
    graph: dict[int, list[int]] = defaultdict(list)
    for a, b in connections:
        graph[a].append(b)
        graph[b].append(a)
    disc = [-1] * n
    low = [0] * n
    bridges: list[list[int]] = []
    timer = 0

    def dfs(node: int, parent: int) -> None:
        nonlocal timer
        disc[node] = low[node] = timer
        timer += 1
        for nxt in graph[node]:
            if nxt == parent:
                continue
            if disc[nxt] == -1:
                dfs(nxt, node)
                low[node] = min(low[node], low[nxt])
                if low[nxt] >= disc[node]:
                    bridges.append([node, nxt])
            else:
                low[node] = min(low[node], disc[nxt])

    for i in range(n):
        if disc[i] == -1:
            dfs(i, -1)
    return sorted(sorted(bridge) for bridge in bridges)


def find_cheapest_price(
    n: int, flights: list[list[int]], src: int, dst: int, k: int
) -> int:
    """LC 787 (Medium-Hard). Cheapest price from ``src`` to ``dst`` using at
    most ``k`` stops, or -1 if unreachable. Bellman-Ford over k + 1 edges.
    """
    inf = float("inf")
    dist = [inf] * n
    dist[src] = 0
    for _ in range(k + 1):
        for u, v, w in flights:
            if dist[u] != inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1 if dist[dst] == inf else int(dist[dst])


def min_cost_connect_points(points: list[list[int]]) -> int:
    """LC 1584 (Medium-Hard). Minimum total cost to connect all points, where
    the cost between two points is their Manhattan distance.
    """
    n = len(points)
    if n <= 1:
        return 0
    seen: set[int] = set()
    heap: list[tuple[int, int]] = [(0, 0)]
    total = 0
    while len(seen) < n:
        cost, i = heapq.heappop(heap)
        seen.add(i)
        total += cost
        for j in range(n):
            if j not in seen:
                distance = abs(points[i][0] - points[j][0]) + abs(
                    points[i][1] - points[j][1]
                )
                heapq.heappush(heap, (distance, j))
    return total
