package com.example.interview;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.Set;

/** Reference fix. See solutions/ANSWERS.md, exercise 4. */
public final class TextWindow {

    private TextWindow() {}

    /** FIX: shrink until the duplicate is gone, and count the window inclusively. */
    public static int longestUnique(String s) {
        Set<Character> window = new HashSet<>();
        int best = 0;
        int left = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            while (window.contains(c)) {
                window.remove(s.charAt(left));
                left++;
            }
            window.add(c);
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    /** FIX: only letters are counted, so whitespace and punctuation cannot index out of range. */
    public static boolean isAnagram(String a, String b) {
        int[] counts = new int[26];
        countLetters(a, counts, 1);
        countLetters(b, counts, -1);
        for (int count : counts) {
            if (count != 0) {
                return false;
            }
        }
        return true;
    }

    private static void countLetters(String s, int[] counts, int delta) {
        for (char c : s.toLowerCase(Locale.ROOT).toCharArray()) {
            if (c >= 'a' && c <= 'z') {
                counts[c - 'a'] += delta;
            }
        }
    }

    /** FIX: LinkedHashMap, so iteration follows the order the characters appeared in. */
    public static Optional<Character> firstUnique(String s) {
        Map<Character, Integer> counts = new LinkedHashMap<>();
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

    /** FIX: split on runs of whitespace, keep every word, and join without a trailing space. */
    public static String reverseWords(String s) {
        String trimmed = s.trim();
        if (trimmed.isEmpty()) {
            return "";
        }
        List<String> words = new ArrayList<>(List.of(trimmed.split("\\s+")));
        Collections.reverse(words);
        return String.join(" ", words);
    }
}
