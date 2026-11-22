package com.example.interview;

import java.time.Duration;
import java.util.HashMap;
import java.util.Map;

/**
 * Fixed-window rate limiter: each key may be granted at most {@code maxRequests}
 * permits per window. Safe to share between threads.
 */
public class RateLimiter {

    private static final class Window {
        long startMillis;
        int count;
    }

    private final int maxRequests;
    private final long windowMillis;
    private Map<String, Window> windows = new HashMap<>();

    public RateLimiter(int maxRequests, Duration window) {
        this.maxRequests = maxRequests;
        this.windowMillis = window.toMillis();
    }

    /** Grants one permit if the key is still under its limit for the current window. */
    public boolean tryAcquire(String key) {
        long now = System.currentTimeMillis();
        Window window = windows.get(key);
        if (window == null) {
            window = new Window();
            window.startMillis = now;
            windows.put(key, window);
        }
        if (now - window.startMillis > windowMillis) {
            window.startMillis = now;
            window.count = 0;
        }
        if (window.count < maxRequests) {
            window.count++;
            return true;
        }
        return false;
    }

    /** Blocks until a permit is available. */
    public void acquire(String key) throws InterruptedException {
        while (!tryAcquire(key)) {
            Thread.sleep(0);
        }
    }

    /** Forgets every window, as used by the admin endpoint. */
    public synchronized void reset() {
        windows = new HashMap<>();
    }

    /** Permits already consumed in the current window, or 0 for an unknown key. */
    public int used(String key) {
        Window window = windows.get(key);
        return window.count;
    }
}
