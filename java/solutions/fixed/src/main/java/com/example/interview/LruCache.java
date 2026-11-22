package com.example.interview;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/** Reference fix. See solutions/ANSWERS.md, exercise 5. */
public final class LruCache<K, V> {

    private final int capacity;
    private final Map<K, V> entries;
    private int hits;
    private int misses;

    public LruCache(int capacity) {
        if (capacity <= 0) {
            throw new IllegalArgumentException("capacity must be positive");
        }
        this.capacity = capacity;
        // FIX: accessOrder = true makes reads count as uses, and the bound is the capacity itself.
        this.entries = new LinkedHashMap<K, V>(16, 0.75f, true) {
            @Override
            protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
                return size() > LruCache.this.capacity;
            }
        };
    }

    public Optional<V> get(K key) {
        // FIX: containsKey decides presence, so a cached null is not mistaken for a miss.
        if (!entries.containsKey(key)) {
            misses++;
            return Optional.empty();
        }
        hits++;
        return Optional.ofNullable(entries.get(key));
    }

    /** FIX: reject null values rather than letting them look like absent entries. */
    public void put(K key, V value) {
        entries.put(Objects.requireNonNull(key), Objects.requireNonNull(value));
    }

    public boolean containsKey(K key) {
        return entries.containsKey(key);
    }

    public int size() {
        return entries.size();
    }

    /** FIX: floating-point division, with the no-calls-yet case defined. */
    public double hitRate() {
        int total = hits + misses;
        return total == 0 ? 0.0 : (double) hits / total;
    }
}
