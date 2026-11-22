# Question index

57 exercises. Every one is a complete, plausible, AI-written solution with planted
bugs, paired with a spec that fails until they are found.

`Caught` = the spec has at least one check that fails on the planted bug.
Full explanations: [python/solutions/ANSWERS.md](python/solutions/ANSWERS.md),
[java/solutions/ANSWERS.md](java/solutions/ANSWERS.md).

## Python — 50 NeetCode Hards

| # | Problem | LC | Category | Bug class | Caught |
| --- | --- | --- | --- | --- | --- |
| 01 | `first_missing_positive` | 41 | arrays | `if` where `while` was needed | yes |
| 02 | `trap` | 42 | two pointers | wrong pointer advanced | yes |
| 03 | `candy` | 135 | greedy | second pass overwrites the first | yes |
| 04 | `max_points` | 149 | math | float slope, div-by-zero | yes |
| 05 | `full_justify` | 68 | strings | off-by-one fit + last line spread | yes |
| 06 | `min_window` | 76 | sliding window | keeps first window, not smallest | yes |
| 07 | `max_sliding_window` | 239 | monotonic deque | front never evicted | yes |
| 08 | `find_substring` | 30 | sliding window | only one alignment scanned | yes |
| 09 | `shortest_subarray` | 862 | prefix + deque | `>` instead of `>=` | yes |
| 10 | `subarrays_with_k_distinct` | 992 | sliding window | at-most-k, not exactly-k | yes |
| 11 | `largest_rectangle_area` | 84 | monotonic stack | missing sentinel flush | yes |
| 12 | `maximal_rectangle` | 85 | monotonic stack | column height never reset | yes |
| 13 | `calculate` | 224 | parsing | digits not accumulated | yes |
| 14 | `longest_valid_parentheses` | 32 | stack | counts total pairs, not longest run | yes |
| 15 | `find_median_sorted_arrays` | 4 | binary search | negative index reads wrong end | yes |
| 16 | `split_array` | 410 | binary search | `>=` in feasibility test | yes |
| 17 | `smallest_distance_pair` | 719 | binary search | counts self-pairs | yes |
| 18 | `count_smaller` | 315 | order statistics | scans the wrong direction | yes |
| 19 | `merge_k_lists` | 23 | heap | no tiebreaker, compares nodes | yes |
| 20 | `MedianFinder` | 295 | heap design | balanced but not partitioned | yes |
| 21 | `smallest_range` | 632 | heap | `<=` breaks the documented tie | yes |
| 22 | `LFUCache` | 460 | design | overwrite not a use + evicts newest | yes |
| 23 | `find_maximized_capital` | 502 | heap greedy | min-heap instead of max-heap | yes |
| 24 | `reverse_k_group` | 25 | linked list | reverses the short tail | yes |
| 25 | `max_path_sum` | 124 | tree DP | no clamp + returns both branches | yes |
| 26 | `serialize` / `deserialize` | 297 | tree design | null markers dropped | yes |
| 27 | `vertical_order` | 987 | tree BFS | groups in BFS order, never sorts | yes |
| 28 | `longest_increasing_path` | 329 | memo DFS | `>=` recurses forever + no memo | yes |
| 29 | `ladder_length` | 127 | BFS | depth never incremented | yes |
| 30 | `alien_order` | 269 | topo sort | invalid-prefix case unhandled | yes |
| 31 | `find_itinerary` | 332 | Hierholzer | takes the largest destination | yes |
| 32 | `swim_in_water` | 778 | Dijkstra-ish | sums instead of max on path | yes |
| 33 | `critical_connections` | 1192 | Tarjan | `>=` on the low-link test | yes |
| 34 | `find_cheapest_price` | 787 | Bellman-Ford | in-place relax breaks the k limit | yes |
| 35 | `min_cost_connect_points` | 1584 | Prim MST | stale heap entry paid twice | yes |
| 36 | `min_distance` | 72 | DP | base column unseeded | yes |
| 37 | `num_distinct` | 115 | DP | forward iteration reuses a char | yes |
| 38 | `max_coins` | 312 | interval DP | current neighbours, not boundaries | yes |
| 39 | `is_match_regex` | 10 | DP | `*` drifts into a free wildcard | yes |
| 40 | `is_match_wildcard` | 44 | DP | `*` matches only the empty run | yes |
| 41 | `is_interleave` | 97 | DP | missing length precondition | yes |
| 42 | `min_cut` | 132 | DP | `cuts[-1]` wraps around | yes |
| 43 | `max_envelopes` | 354 | LIS | ascending tie-break lets ties nest | yes |
| 44 | `word_break_ii` | 140 | DP + DFS | trailing space on every sentence | yes |
| 45 | `calculate_minimum_hp` | 174 | DP | health not clamped to 1 | yes |
| 46 | `job_scheduling` | 1235 | DP + bisect | `bisect_left` rejects touching jobs | yes |
| 47 | `min_interval` | 1851 | heap sweep | queries swept unsorted | yes |
| 48 | `employee_free_time` | 759 | intervals | running end not a max | yes |
| 49 | `find_words` | 212 | trie + DFS | board never restored | yes |
| 50 | `solve_n_queens` | 51 | backtracking | anti-diagonal forgotten | yes |

## Java — 7 engineering-flavoured exercises

Less algorithmic, more "would this survive code review": collections, money,
concurrency, API contracts.

| # | Exercise | Difficulty | Bugs | Probes |
| --- | --- | --- | --- | --- |
| 1 | `OrderBook` | easy | 8 | `Collectors.toMap`, string identity, encapsulation, float money |
| 2 | `IntervalScheduler` | easy–medium | 6 | sort keys, half-open bounds, heap direction |
| 3 | `GraphRoutes` | medium | 7 | BFS vs DFS, visited sets, path rebuild, level counting |
| 4 | `TextWindow` | medium | 7 | window invariants, charset assumptions, map ordering |
| 5 | `LruCache` | medium | 6 | contract reading, eviction policy, integer division |
| 6 | `RateLimiter` | hard | 7 | atomicity, publication, check-then-act, lock scope |
| 7 | `PaymentProcessor` | medium–hard | 7 | immutability, `BigDecimal` scale vs value, PII in logs |

## Coverage by bug class

Useful for picking a set that is not all the same lesson twice.

| Bug class | Problems |
| --- | --- |
| Off-by-one / boundary operator | 01, 05, 09, 16, 17, 33, 46 |
| Wrong direction of iteration | 02, 18, 37, 45 |
| Invariant silently violated | 06, 07, 20, 34, 43, 48 |
| Recurrence subtly wrong | 36, 38, 39, 40, 41, 42 |
| State not restored / stale state | 24, 35, 49, 50 |
| Spec read too loosely | 10, 21, 22, 26, 27, 30, 44, 47 |
| Crashes rather than lies | 04, 19, 26, 28 |
| Concurrency | Java 6 |
| Money and precision | Java 1, Java 7 |
