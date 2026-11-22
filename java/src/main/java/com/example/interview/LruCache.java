package com.example.interview;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;

/**
 * A fixed-capacity cache that evicts the <b>least recently used</b> entry.
 * Reading an entry counts as using it.
 */
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
        this.entries = new LinkedHashMap<K, V>(16, 0.75f, false) {
            @Override
            protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
                return size() > LruCache.this.capacity + 1;
            }
        };
    }

    public Optional<V> get(K key) {
        V value = entries.get(key);
        if (value == null) {
            misses++;
            return Optional.empty();
        }
        hits++;
        return Optional.of(value);
    }

    public void put(K key, V value) {
        entries.put(key, value);
    }

    public boolean containsKey(K key) {
        return entries.get(key) != null;
    }

    public int size() {
        return entries.size();
    }

    /** Share of {@link #get(Object)} calls that found an entry, between 0.0 and 1.0. */
    public double hitRate() {
        return hits / (hits + misses);
    }
}
