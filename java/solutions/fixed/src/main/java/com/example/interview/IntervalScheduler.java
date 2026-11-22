package com.example.interview;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;

/** Reference fix. See solutions/ANSWERS.md, exercise 2. */
public final class IntervalScheduler {

    public record Interval(int start, int end) {}

    private IntervalScheduler() {}

    /** FIX: sort by start, join touching ranges with <=, and append the final interval. */
    public static List<Interval> merge(List<Interval> intervals) {
        if (intervals.isEmpty()) {
            return List.of();
        }
        List<Interval> sorted = new ArrayList<>(intervals);
        sorted.sort(Comparator.comparingInt(Interval::start));

        List<Interval> merged = new ArrayList<>();
        Interval current = sorted.get(0);
        for (int i = 1; i < sorted.size(); i++) {
            Interval next = sorted.get(i);
            if (next.start() <= current.end()) {
                current = new Interval(current.start(), Math.max(current.end(), next.end()));
            } else {
                merged.add(current);
                current = next;
            }
        }
        merged.add(current);
        return List.copyOf(merged);
    }

    /** FIX: a min-heap, so the room that frees up earliest is the one we reuse. */
    public static int minRooms(List<Interval> meetings) {
        List<Interval> sorted = new ArrayList<>(meetings);
        sorted.sort(Comparator.comparingInt(Interval::start));

        PriorityQueue<Integer> endTimes = new PriorityQueue<>();
        for (Interval meeting : sorted) {
            if (!endTimes.isEmpty() && endTimes.peek() <= meeting.start()) {
                endTimes.poll();
            }
            endTimes.add(meeting.end());
        }
        return endTimes.size();
    }

    /** FIX: sort once and compare neighbours — O(n log n), and no self-comparison. */
    public static boolean canAttendAll(List<Interval> meetings) {
        List<Interval> sorted = new ArrayList<>(meetings);
        sorted.sort(Comparator.comparingInt(Interval::start));
        for (int i = 1; i < sorted.size(); i++) {
            if (overlaps(sorted.get(i - 1), sorted.get(i))) {
                return false;
            }
        }
        return true;
    }

    /** FIX: strict comparisons, because the bounds are half-open. */
    private static boolean overlaps(Interval a, Interval b) {
        return a.start() < b.end() && b.start() < a.end();
    }
}
