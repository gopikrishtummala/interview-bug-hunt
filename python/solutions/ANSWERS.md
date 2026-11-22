# Interviewer's key — Python, 50 NeetCode Hards

Do not hand this to the candidate.

Baseline: **77 of 156 checks fail**, and **all 50 problems have at least one failing
check**. Working fixes are in `solutions/fixed/` (every change carries a `# FIX:`
comment) and run **156/156**.

Format: **bug → why it bites → fix**. Problems with two planted bugs say so.

---

## Arrays and strings

**01 `first_missing_positive`** — `if` instead of `while` around the cyclic-sort swap.
One swap can drop *another* misplaced value into slot `i`, and the loop has already
moved on. `[3,4,-1,1]` → 1 instead of 2. → `while`.

**02 `trap`** — advances the **taller** side (`if left_max > right_max`). The whole
two-pointer argument is that the *shorter* side's running max bounds the water there, so
that side is the one safe to move. Returns 13 instead of 6. → `if left_max < right_max`.

**03 `candy`** — the right-to-left pass **assigns** instead of taking the max, wiping out
the left pass wherever the left pass was larger. `[1,2,3,4,1]` → 9 instead of 11. →
`candies[i] = max(candies[i], candies[i+1] + 1)`.

**04 `max_points`** — a float slope `dy / dx`. `ZeroDivisionError` on a vertical line,
and float keys silently merge lines that are merely nearly parallel. → a reduced integer
`(dx // g, dy // g)` pair with the sign normalised, so `1/2` and `-1/-2` agree.

**05 `full_justify`** — *two bugs.* The fit test counts `len(line) - 1` gaps, so a line
can exceed `max_width` by one character; and the final line is pushed through the
justifier instead of being left-justified. → `length + len(line) + len(word)`, and
`" ".join(line).ljust(max_width)` for the last line.

## Sliding window

**06 `min_window`** — `if end == 0` keeps the **first** valid window, not the shortest.
`"ADOBECODEBANC"` → `"ADOBEC"` instead of `"BANC"`. → also test
`right - left < end - start`.

**07 `max_sliding_window`** — the front index is never evicted when it falls out of the
window, so a maximum that has already slid past is still reported. `[7,2,4], k=2` →
`[7,7]` instead of `[7,4]`. → `if queue[0] <= i - k: queue.popleft()`.

**08 `find_substring`** — only the alignment starting at index 0 is scanned. Any match
whose start is not a multiple of the word length is invisible. → loop
`for offset in range(width)`, resetting the window for each offset.

**09 `shortest_subarray`** — `> k` instead of `>= k`: a subarray summing to *exactly* `k`
is rejected. `[1], k=1` → -1. → `>=`.

**10 `subarrays_with_k_distinct`** — returns at-most-k instead of exactly-k. 12 instead
of 7. → `_at_most(nums, k) - _at_most(nums, k - 1)`. The point of the problem is that one
window cannot count "exactly k" directly.

## Stacks

**11 `largest_rectangle_area`** — no sentinel, so bars still on the stack when the loop
ends are never measured. A monotonically increasing histogram returns **0**. → iterate
`heights + [0]`.

**12 `maximal_rectangle`** — `heights[j] += 1 if cell == "1" else 0` never **resets** a
column on a zero, so ones separated by a zero are treated as contiguous. → assign
`heights[j] + 1` or `0`.

**13 `calculate`** — `num = int(char)` overwrites instead of accumulating, so `"42"`
evaluates to 2. Every single-digit test passes. → `num = num * 10 + int(char)`.

**14 `longest_valid_parentheses`** — counts the **total** number of matched pairs rather
than the longest *contiguous* run. `"()((" `-style inputs pass; `"()(()"` gives 4 instead
of 2. → a stack of indices seeded with `-1`, measuring `i - stack[-1]`.

## Binary search

**15 `find_median_sorted_arrays`** — the swap that makes `a` the shorter array is missing,
so `j = half - i` can go negative and Python's negative indexing reads from the **wrong
end of `b`** instead of raising. A silently wrong median, not a crash. → swap when
`len(a) > len(b)`.

**16 `split_array`** — `current + value >= cap` treats a part that exactly fills the cap
as overflowing, so the answer comes back one too large (19 instead of 18). → `>`.

**17 `smallest_distance_pair`** — `total += right - left + 1` counts each element paired
with **itself**, inflating every count by n, so the search always collapses to 0. →
`right - left`.

**18 `count_smaller`** — scans left to right and never reverses, so it counts smaller
elements *before* each index. `[5,2,6,1]` → `[0,0,2,0]` instead of `[2,1,1,0]`. → iterate
`reversed(nums)`, then reverse the result.

## Heaps and design

**19 `merge_k_lists`** — pushes `(node.val, node)`. When two heads tie, `heapq` falls
through to comparing `ListNode` objects → `TypeError: '<' not supported`. → push
`(val, list_index, node)`.

**20 `MedianFinder`** — pushes into whichever heap is currently shorter. The heaps end up
**balanced but not partitioned**: `small` can hold values larger than everything in
`large`, so the tops are not the median. Descending input gives 5.0 instead of 3.0. →
push onto `small`, move its max into `large`, then rebalance. The best question in the
set: the sizes being right is exactly what hides it.

**21 `smallest_range`** — `<=` when comparing widths, so a later range of equal width
replaces the earlier one, against the documented tie-break. → `<`.

**22 `LFUCache`** — *two bugs.* `put` on an existing key updates the value without
counting as a use; and eviction calls `popitem(last=True)`, removing the **most** recently
used key in the least-frequent bucket instead of the least. → `_touch` on overwrite, and
`popitem(last=False)`.

**23 `find_maximized_capital`** — profits go into a **min**-heap and the smallest is
popped, so it picks the least profitable affordable project. 3 instead of 4. → negate for
a max-heap.

## Linked lists and trees

**24 `reverse_k_group`** — reverses `count` nodes even when `count < k`, so the short tail
is reversed too. The guard is not an optimisation, it is the spec. → `if count < k: return
head`.

**25 `max_path_sum`** — *two bugs.* Negative branches are not clamped to 0, so a negative
child is forced into the path; and the value handed back to the parent adds **both**
branches, which is not a path through the parent. → `max(gain(child), 0)` and return
`node.val + max(left, right)`.

**26 `serialize`** — null markers are dropped. `"1,2,3"` is ambiguous between several
shapes, so `deserialize` either runs out of tokens (`StopIteration`) or rebuilds a left
spine; the empty tree serialises to `""` and then `int("")` raises. → emit `"#"` for
`None`. Ask what property of an encoding makes it invertible.

**27 `vertical_order`** — groups nodes in **BFS order** instead of sorting by
`(col, row, value)`, so columns come out in discovery order and a column reached twice
becomes two separate groups. → sort `nodes` first.

**28 `longest_increasing_path`** — *two bugs.* `>=` instead of `>` lets two equal
neighbours recurse into each other forever (`RecursionError` on the classic input), and
there is no memo, so even once fixed it is exponential. → strict `>` plus a cache.

## Graphs

**29 `ladder_length`** — enqueues neighbours with the same `steps` and never increments,
so every reachable word is at distance 1. → `steps + 1`.

**30 `alien_order`** — no check for a word that follows its own prefix (`["abc","ab"]`),
which is a contradictory dictionary and must give `""`. → the `for ... else` branch
comparing lengths. (The cycle check at the end is already correct — point that out; the
candidate has to notice *which* invalid case is unhandled.)

**31 `find_itinerary`** — sorts ascending and then `pop()`s from the **end**, taking the
largest destination each time: the exact reverse of the lexically smallest itinerary. →
sort descending so `pop()` yields the smallest.

**32 `swim_in_water`** — `time += height` accumulates instead of tracking the **maximum**
height along the path. 6 instead of 3 on a 2×2. → `time = max(time, height)`.

**33 `critical_connections`** — `low[nxt] >= disc[node]`. Equality means the child can
reach back to this very node, i.e. it sits on a cycle, so the edge is **not** a bridge. A
triangle is reported as having one. → strict `>`.

**34 `find_cheapest_price`** — relaxes `dist` **in place**, so a single Bellman-Ford round
can chain several edges and the k-stop limit is not enforced. With `k=0` it still finds a
two-hop route. → relax against a snapshot of the previous round.

**35 `min_cost_connect_points`** — no stale-entry guard, so a node already in the tree is
paid for a second time. → `if i in seen: continue` after the pop.

## Dynamic programming

**36 `min_distance`** — only the first row is seeded; `dp[i][0]` stays 0, so deleting a
whole prefix is free. `min_distance("abc", "")` → 0. → seed the first column too.

**37 `num_distinct`** — iterates `j` **forward**, so one character of `s` updates `dp[j]`
and then `dp[j+1]` in the same row, being consumed twice. → iterate `j` downwards. The
same backwards-iteration trick as 0/1 knapsack.

**38 `max_coins`** — multiplies by `values[k-1]` and `values[k+1]`, the *current*
neighbours, instead of the interval boundaries `values[left]` and `values[right]`. The
entire reason the recurrence works is that `k` is the **last** balloon burst in the open
range, so its neighbours are the untouched boundaries. → `values[left] * values[k] *
values[right]`.

**39 `is_match_regex`** — `*` is treated as a free-floating wildcard
(`dp[i][j-1] or dp[i-1][j]`) rather than "zero or more of the preceding element", so
`"mississippi"` matches `"mis*is*p*."`. → index back two for the zero case, and check
`p[j-2]` against `s[i-1]` for the one-more case.

**40 `is_match_wildcard`** — `*` can only match the **empty** sequence (`dp[i][j-1]`), so
`"aa"` against `"*"` is False. → `dp[i-1][j] or dp[i][j-1]`.

**41 `is_interleave`** — the length check is missing. It is not an optimisation: without
it a short `s1 + s2` can match a *prefix* of `s3` and return True. → compare lengths
first.

**42 `min_cut`** — no `start == 0` special case, so `cuts[start - 1]` becomes `cuts[-1]`,
which in Python is the **last element of the list** — a half-built value from a future
index. `"aab"` → 2 instead of 1. A great illustration of negative indexing hiding an
off-by-one. → `best = 0 if start == 0 else min(best, cuts[start-1] + 1)`.

**43 `max_envelopes`** — sorts height **ascending** within equal widths, so two envelopes
of the same width look nestable. → `key=lambda e: (e[0], -e[1])`.

**44 `word_break_ii`** — always joins with a space, so every sentence carries a trailing
space. → add the separator only when the tail is non-empty.

**45 `calculate_minimum_hp`** — never clamps the requirement to a minimum of 1, so a room
with a large bonus yields zero or negative required health. → `max(1, need)`.

## Greedy and intervals

**46 `job_scheduling`** — `bisect_left` rejects a predecessor that ends exactly when this
job starts, although the docstring says touching jobs do not overlap. 100 instead of 150.
→ `bisect_right`.

**47 `min_interval`** — sweeps the queries **in the order given** while the interval
pointer only moves forward, so an out-of-order query sees an under-filled heap. → sort
for the sweep, keep the answers in a dict, return them in the caller's order.

**48 `employee_free_time`** — `end = finish` instead of `max(end, finish)`. An interval
nested inside an earlier one drags the running end backwards and invents a gap that is
not free. → `max`.

## Backtracking

**49 `find_words`** — the cell is never restored after the DFS, so the board keeps its
`"#"` marks and every later starting square walks a holed board. The first word is found;
the rest are not. → `board[r][c] = char` on the way out.

**50 `solve_n_queens`** — only `row - col` is tracked; the anti-diagonal `row + col` is
forgotten, so placements with queens attacking along the other diagonal are reported.
`n=4` yields more than two solutions, `n=8` more than 92. → track both sets.

---

## Bugs the spec does *not* catch

Worth asking about when someone gets a problem clean quickly:

- **28** `longest_increasing_path` — once `>=` is fixed to `>`, the missing memo is only a
  performance bug, and the test inputs are tiny. Ask for the complexity.
- **30** `alien_order` — the `break` after the first differing character pair is present
  and correct here; ask what would break without it (edges implied by positions after the
  first difference, which carry no information).
- **44** `word_break_ii` — the memo is present. Ask why it matters, and for the input that
  makes it matter (`"aaaa…"` with `["a","aa","aaa"]`).
- **04** `max_points` — even with integer slopes, this is O(n²) and the key normalisation
  is easy to get subtly wrong for `(0, -1)` vs `(0, 1)`.
- None of these are thread-safe or input-validating; for 22 `LFUCache` ask what happens
  with `capacity=0`.

## The through-line

Every bug here reads as correct, survives a happy-path test, and sits in code that is
better commented than most production code. That is the failure mode of generated
solutions to hard problems: the shape of the algorithm is right and one invariant is
quietly violated — the wrong pointer, the wrong operator, the wrong direction of
iteration, the state that is never restored.

The skill under test is not "can you invent the algorithm". It is "can you tell whether
this code actually does what it says".
