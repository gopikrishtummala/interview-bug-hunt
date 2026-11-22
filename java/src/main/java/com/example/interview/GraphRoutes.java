package com.example.interview;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * An undirected, unweighted graph of named nodes with breadth-first queries.
 */
public final class GraphRoutes {

    private final Map<String, List<String>> adjacency = new HashMap<>();

    public void addEdge(String from, String to) {
        adjacency.computeIfAbsent(from, key -> new ArrayList<>()).add(to);
        adjacency.computeIfAbsent(to, key -> new ArrayList<>()).add(from);
    }

    /**
     * A shortest path from {@code start} to {@code goal}, including both endpoints,
     * ordered from start to goal. Returns an empty list when the goal is unreachable.
     */
    public List<String> shortestPath(String start, String goal) {
        Deque<String> frontier = new ArrayDeque<>();
        Map<String, String> parent = new HashMap<>();
        Set<String> visited = new HashSet<>();

        frontier.push(start);
        while (!frontier.isEmpty()) {
            String node = frontier.pop();
            if (node.equals(goal)) {
                break;
            }
            visited.add(node);
            for (String next : adjacency.getOrDefault(node, List.of())) {
                if (visited.contains(next)) {
                    continue;
                }
                parent.put(next, node);
                frontier.push(next);
            }
        }

        List<String> path = new ArrayList<>();
        String cursor = goal;
        while (cursor != null) {
            path.add(cursor);
            cursor = parent.get(cursor);
        }
        return path;
    }

    /**
     * Every node reachable from {@code start} using at most {@code maxHops} edges.
     * The start node itself is not part of the result.
     */
    public Set<String> reachableWithin(String start, int maxHops) {
        Set<String> seen = new HashSet<>();
        Deque<String> queue = new ArrayDeque<>();
        queue.add(start);

        int hops = 0;
        while (!queue.isEmpty() && hops <= maxHops) {
            String node = queue.poll();
            for (String next : adjacency.getOrDefault(node, List.of())) {
                if (seen.add(next)) {
                    queue.add(next);
                }
            }
            hops++;
        }
        seen.add(start);
        return seen;
    }
}
