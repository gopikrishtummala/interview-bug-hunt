package com.example.interview;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Optional;
import java.util.Set;

/**
 * String scanning problems solved with a sliding window and frequency counts.
 */
public final class TextWindow {

    private TextWindow() {}

    /** Length of the longest substring of {@code s} with no repeated character. */
    public static int longestUnique(String s) {
        Set<Character> window = new HashSet<>();
        int best = 0;
        int left = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            if (window.contains(c)) {
                window.remove(s.charAt(left));
                left++;
            }
            window.add(c);
            best = Math.max(best, right - left);
        }
        return best;
    }

    /** True when {@code a} and {@code b} are anagrams, ignoring case and whitespace. */
    public static boolean isAnagram(String a, String b) {
        int[] counts = new int[26];
        for (char c : a.toLowerCase().toCharArray()) {
            counts[c - 'a']++;
        }
        for (char c : b.toLowerCase().toCharArray()) {
            counts[c - 'a']--;
        }
        for (int count : counts) {
            if (count != 0) {
                return false;
            }
        }
        return true;
    }

    /**
     * The first character of {@code s} that occurs exactly once, in the order the
     * characters appear in the input. Empty when every character repeats.
     */
    public static Optional<Character> firstUnique(String s) {
        Map<Character, Integer> counts = new HashMap<>();
        for (char c : s.toCharArray()) {
            counts.merge(c, 1, Integer::sum);
        }
        for (Map.Entry<Character, Integer> entry : counts.entrySet()) {
            if (entry.getValue() == 1) {
                return Optional.of(entry.getKey());
            }
        }
        return Optional.empty();
    }

    /** Reverses the order of whitespace-separated words, collapsing runs of spaces. */
    public static String reverseWords(String s) {
        String[] words = s.trim().split(" ");
        StringBuilder out = new StringBuilder();
        for (int i = words.length - 1; i > 0; i--) {
            out.append(words[i]).append(" ");
        }
        return out.toString();
    }
}
