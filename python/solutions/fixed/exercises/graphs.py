"""Reference fixes — graphs."""

from __future__ import annotations

import heapq
from collections import defaultdict, deque
from string import ascii_lowercase


def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    """LC 127 (Hard). Shortest transformation length, inclusive of both ends."""
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
                # FIX: mark on enqueue, or the same word is queued many times.
                if nxt in words and nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, steps + 1))
    return 0


def alien_order(words: list[str]) -> str:
    """LC 269 (Hard). Letter order implied by a sorted alien dictionary."""
    adjacency: dict[str, set[str]] = {c: set() for word in words for c in word}
    indegree: dict[str, int] = {c: 0 for c in adjacency}
    for first, second in zip(words, words[1:]):
        for a, b in zip(first, second):
            if a != b:
                if b not in adjacency[a]:
                    adjacency[a].add(b)
                    indegree[b] += 1
                # FIX: only the first differing pair carries information.
                break
        else:
            # FIX: a prefix after its own extension is an invalid dictionary.
            if len(second) < len(first):
                return ""
    queue = deque(sorted(c for c in indegree if indegree[c] == 0))
    out: list[str] = []
    while queue:
        char = queue.popleft()
        out.append(char)
        for nxt in sorted(adjacency[char]):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    # FIX: a short result means a cycle, which has no valid order.
    return "".join(out) if len(out) == len(adjacency) else ""


def find_itinerary(tickets: list[list[str]]) -> list[str]:
    """LC 332 (Hard). Use every ticket once, smallest lexical itinerary from JFK."""
    graph: dict[str, list[str]] = defaultdict(list)
    # FIX: reverse-sorted, so pop() takes the smallest destination.
    for src, dst in sorted(tickets, reverse=True):
        graph[src].append(dst)
    route: list[str] = []

    def visit(airport: str) -> None:
        while graph[airport]:
            visit(graph[airport].pop())
        # FIX: Hierholzer - append on the way out, then reverse.
        route.append(airport)

    visit("JFK")
    return route[::-1]


def swim_in_water(grid: list[list[int]]) -> int:
    """LC 778 (Hard). Least time to reach the bottom-right corner."""
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]
    seen = {(0, 0)}
    time = 0
    while heap:
        height, r, c = heapq.heappop(heap)
        # FIX: the answer is the highest cell on the path, not the sum.
        time = max(time, height)
        if r == n - 1 and c == n - 1:
            return time
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
                seen.add((nr, nc))
                heapq.heappush(heap, (grid[nr][nc], nr, nc))
    return -1


def critical_connections(n: int, connections: list[list[int]]) -> list[list[int]]:
    """LC 1192 (Hard). Bridges of an undirected graph (Tarjan)."""
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
                # FIX: strictly greater - equality means a cycle, not a bridge.
                if low[nxt] > disc[node]:
                    bridges.append([node, nxt])
            else:
                # FIX: a back edge contributes disc, never low.
                low[node] = min(low[node], disc[nxt])

    for i in range(n):
        if disc[i] == -1:
            dfs(i, -1)
    return sorted(sorted(bridge) for bridge in bridges)


def find_cheapest_price(
    n: int, flights: list[list[int]], src: int, dst: int, k: int
) -> int:
    """LC 787 (Medium-Hard). Cheapest route using at most k stops."""
    inf = float("inf")
    dist = [inf] * n
    dist[src] = 0
    # FIX: k stops means k + 1 edges.
    for _ in range(k + 1):
        # FIX: relax against last round's distances, or one pass uses too many hops.
        nxt = dist[:]
        for u, v, w in flights:
            if dist[u] != inf and dist[u] + w < nxt[v]:
                nxt[v] = dist[u] + w
        dist = nxt
    return -1 if dist[dst] == inf else int(dist[dst])


def min_cost_connect_points(points: list[list[int]]) -> int:
    """LC 1584 (Medium-Hard). Minimum spanning tree under Manhattan distance."""
    n = len(points)
    if n <= 1:
        return 0
    seen: set[int] = set()
    heap: list[tuple[int, int]] = [(0, 0)]
    total = 0
    while len(seen) < n:
        cost, i = heapq.heappop(heap)
        # FIX: skip stale heap entries instead of paying for a node twice.
        if i in seen:
            continue
        seen.add(i)
        total += cost
        for j in range(n):
            if j not in seen:
                distance = abs(points[i][0] - points[j][0]) + abs(
                    points[i][1] - points[j][1]
                )
                heapq.heappush(heap, (distance, j))
    return total
