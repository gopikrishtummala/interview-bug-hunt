package com.example.interview;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;

/** Reference fix. See solutions/ANSWERS.md, exercise 3. */
public final class GraphRoutes {

    private final Map<String, List<String>> adjacency = new HashMap<>();

    public void addEdge(String from, String to) {
        adjacency.computeIfAbsent(from, key -> new ArrayList<>()).add(to);
        adjacency.computeIfAbsent(to, key -> new ArrayList<>()).add(from);
    }

    /**
     * FIX: FIFO queue (so it is really breadth-first), visited marked at enqueue time
     * so each node gets exactly one parent, the path reversed, and an unreachable goal
     * reported as an empty list.
     */
    public List<String> shortestPath(String start, String goal) {
        if (start.equals(goal)) {
            return List.of(start);
        }

        Deque<String> queue = new ArrayDeque<>();
        Map<String, String> parent = new HashMap<>();
        Set<String> visited = new HashSet<>();

        queue.addLast(start);
        visited.add(start);
        boolean found = false;

        while (!queue.isEmpty() && !found) {
            String node = queue.pollFirst();
            for (String next : adjacency.getOrDefault(node, List.of())) {
                if (!visited.add(next)) {
                    continue;
                }
                parent.put(next, node);
                if (next.equals(goal)) {
                    found = true;
                    break;
                }
                queue.addLast(next);
            }
        }

        if (!found) {
            return List.of();
        }

        LinkedList<String> path = new LinkedList<>();
        for (String cursor = goal; cursor != null; cursor = parent.get(cursor)) {
            path.addFirst(cursor);
        }
        return List.copyOf(path);
    }

    /** FIX: drain one whole level per hop, and leave the start node out of the result. */
    public Set<String> reachableWithin(String start, int maxHops) {
        Set<String> seen = new HashSet<>();
        Deque<String> queue = new ArrayDeque<>();

        queue.addLast(start);
        seen.add(start);

        for (int hop = 0; hop < maxHops && !queue.isEmpty(); hop++) {
            int levelSize = queue.size();
            for (int i = 0; i < levelSize; i++) {
                String node = queue.pollFirst();
                for (String next : adjacency.getOrDefault(node, List.of())) {
                    if (seen.add(next)) {
                        queue.addLast(next);
                    }
                }
            }
        }

        Set<String> reachable = new HashSet<>(seen);
        reachable.remove(start);
        return reachable;
    }
}
