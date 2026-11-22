package com.example.interview;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;

/**
 * Classic interval problems.
 *
 * <p>Every interval is half-open: {@code [start, end)}. Two intervals that merely
 * touch (for example {@code [1,3)} and {@code [3,5)}) do <b>not</b> overlap, but
 * {@link #merge(List)} still joins them because the result is a coverage range.
 */
public final class IntervalScheduler {

    public record Interval(int start, int end) {}

    private IntervalScheduler() {}

    /**
     * Merges overlapping and touching intervals.
     * The result is sorted by start and contains no two joinable intervals.
     */
    public static List<Interval> merge(List<Interval> intervals) {
        if (intervals.isEmpty()) {
            return List.of();
        }
        List<Interval> sorted = new ArrayList<>(intervals);
        sorted.sort(Comparator.comparingInt(Interval::end));

        List<Interval> merged = new ArrayList<>();
        Interval current = sorted.get(0);
        for (int i = 1; i < sorted.size(); i++) {
            Interval next = sorted.get(i);
            if (next.start() < current.end()) {
                current = new Interval(current.start(), Math.max(current.end(), next.end()));
            } else {
                merged.add(current);
                current = next;
            }
        }
        return merged;
    }

    /** Minimum number of rooms required to host every meeting without a clash. */
    public static int minRooms(List<Interval> meetings) {
        List<Interval> sorted = new ArrayList<>(meetings);
        sorted.sort(Comparator.comparingInt(Interval::start));

        PriorityQueue<Integer> endTimes = new PriorityQueue<>(Comparator.reverseOrder());
        for (Interval meeting : sorted) {
            if (!endTimes.isEmpty() && endTimes.peek() <= meeting.start()) {
                endTimes.poll();
            }
            endTimes.add(meeting.end());
        }
        return endTimes.size();
    }

    /** True when one person can attend every meeting, i.e. no two of them overlap. */
    public static boolean canAttendAll(List<Interval> meetings) {
        for (int i = 0; i < meetings.size(); i++) {
            for (int j = i; j < meetings.size(); j++) {
                if (overlaps(meetings.get(i), meetings.get(j))) {
                    return false;
                }
            }
        }
        return true;
    }

    private static boolean overlaps(Interval a, Interval b) {
        return a.start() <= b.end() && b.start() <= a.end();
    }
}
