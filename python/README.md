# Python debugging interview — 50 NeetCode Hards

A LeetCode substitute. The candidate does not invent an algorithm: they are handed
**50 confident, idiomatic, AI-written Python solutions to hard problems** and a failing
spec, and have to find out why each one is wrong.

Every function is complete and plausible. Every docstring states the real contract.
The bugs are the ones models actually produce on hard problems: the wrong pointer
advanced, `>=` where `>` was meant, a monotonic deque that never evicts, a `*` that
drifts from "zero or more of the preceding element" into a free wildcard, a Tarjan
low-link compared with the wrong operator, heaps that are balanced but not partitioned.

**Verified on CPython 3.12:** the kit fails **77 of 156 checks**, and **all 50 problems
have at least one failing check** — none is accidentally correct. The reference fixes in
`solutions/fixed/` pass **156/156**, so every assertion is reachable.

## Run it

```powershell
python verify.py
```

```powershell
python verify.py -q
```

`-q` prints one line per problem (`pass`/`FAIL` and a `k/n` count) instead of every
case — that is the scoreboard to work against. Add `--fixed` to run the same spec
against the reference solutions. No dependencies, no pytest, Python 3.9+.

## Layout

```
exercises/
  support.py            ListNode / TreeNode and builders — fixtures, known good
  arrays_strings.py     01-05
  windows.py            06-10
  stacks.py             11-14
  searching.py          15-18
  heaps_design.py       19-23
  linked_trees.py       24-28
  graphs.py             29-35
  dynamic.py            36-45
  greedy_intervals.py   46-48
  backtracking.py       49-50
verify.py               the spec as 156 assertions — do not edit
solutions/ANSWERS.md    interviewer's key: every bug, why it bites, the fix
solutions/fixed/        working implementations, each change marked `# FIX:`
```

See [../QUESTIONS.md](../QUESTIONS.md) for the full index with LeetCode numbers.

## How to run the interview

Do **not** hand over all 50. Pick 2–4 by what you want to probe.

| Phase | Time | Watching for |
| --- | --- | --- |
| Read one function cold, think aloud | 5 min | Do they reconstruct the intended algorithm before hunting? Do they read the docstring as the contract? |
| Predict the failure before running | 5 min | Can they find it by reading, or only by bisecting output? |
| Fix until the problem is clean | 15 min | Minimal targeted fix, or rewrite-from-scratch panic? |
| Explain the mechanism | 5 min | "The invariant was X and this line breaks it", not "I changed it and it passed" |

**Suggested sets**

- *Invariant reasoning:* 02 `trap`, 07 `max_sliding_window`, 20 `MedianFinder`
- *Boundary conditions:* 09 `shortest_subarray`, 16 `split_array`, 17 `smallest_distance_pair`, 46 `job_scheduling`
- *DP recurrences:* 38 `max_coins`, 39 `is_match_regex`, 40 `is_match_wildcard`, 42 `min_cut`
- *Graph subtlety:* 31 `find_itinerary`, 33 `critical_connections`, 34 `find_cheapest_price`
- *State restoration:* 49 `find_words`, 50 `solve_n_queens`, 24 `reverse_k_group`
- *Spec reading, not algorithms:* 22 `LFUCache`, 26 `serialize`, 48 `employee_free_time`

**Strong signals**

- Reconstructs the intended invariant and then points at the line that violates it.
- On 20, says the two heaps are *balanced but not partitioned* — the hard part is seeing
  that the sizes being right is exactly what hides the bug.
- On 38, explains why k must be the *last* balloon burst in the range, which is the
  insight the buggy line quietly discards.
- Notices that 15 reads `b[-1]` through a negative index rather than raising — a silently
  wrong answer, not a crash.
- Flags the bugs the spec does *not* catch (the key marks them).

**Weak signals**

- Rewrites the function from memory instead of locating the defect. (It may even pass —
  ask them what the bug *was*.)
- Treats a green problem as proof the code is right.
- Reaches for `print` before reading the recurrence.
- Edits `verify.py`.

## Variants

- **Review mode:** no running. They list suspected bugs with severity; then run it together.
- **Write-the-test mode:** hand them a fixed function and ask for the case that would
  have caught the original bug.
- **Timed triage:** 30 minutes, 8 problems, how many can they get clean — rewards reading
  speed over depth.
