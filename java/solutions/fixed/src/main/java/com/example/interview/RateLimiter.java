package com.example.interview;

import java.time.Duration;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Reference fix. See solutions/ANSWERS.md, exercise 6.
 *
 * <p>One lock per key, held across the whole decide-and-increment, so the check and
 * the act cannot be split. A production answer would reach for Guava's RateLimiter,
 * Bucket4j, or a Redis counter instead of hand-rolling this.
 */
public class RateLimiter {

    private static final class Window {
        long startNanos;
        int count;

        Window(long startNanos) {
            this.startNanos = startNanos;
        }
    }

    private final int maxRequests;
    private final long windowNanos;
    // FIX: concurrent map, and final so there is nothing to publish unsafely.
    private final Map<String, Window> windows = new ConcurrentHashMap<>();

    public RateLimiter(int maxRequests, Duration window) {
        this.maxRequests = maxRequests;
        this.windowNanos = window.toNanos();
    }

    /** FIX: computeIfAbsent creates the window once, and the lock makes the rest atomic. */
    public boolean tryAcquire(String key) {
        // FIX: nanoTime is monotonic; currentTimeMillis can step backwards.
        long now = System.nanoTime();
        Window window = windows.computeIfAbsent(key, ignored -> new Window(now));
        synchronized (window) {
            if (now - window.startNanos >= windowNanos) {
                window.startNanos = now;
                window.count = 0;
            }
            if (window.count < maxRequests) {
                window.count++;
                return true;
            }
            return false;
        }
    }

    /** FIX: wait for the window to roll over instead of spinning on sleep(0). */
    public void acquire(String key) throws InterruptedException {
        while (!tryAcquire(key)) {
            Thread.sleep(Math.max(1L, windowNanos / 1_000_000L / 10L));
        }
    }

    public void reset() {
        windows.clear();
    }

    /** FIX: an unknown key is 0, as documented, and the read happens under the lock. */
    public int used(String key) {
        Window window = windows.get(key);
        if (window == null) {
            return 0;
        }
        synchronized (window) {
            return window.count;
        }
    }
}
