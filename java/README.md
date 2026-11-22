# Java debugging interview — a LeetCode substitute

Instead of inventing an algorithm from scratch, the candidate is handed **seven
plausible, confident, AI-written Java classes** and a failing spec. The job is the
one the job actually is: read unfamiliar code, work out what it was supposed to do,
find the bugs, fix them, and explain them.

Every file compiles. Every file looks reviewed. Nothing here is a typo — the bugs
are the ones models and humans actually produce: wrong sort key, off-by-one window,
`==` on boxed/interned values, `BigDecimal` immutability, `LinkedHashMap` access
order, integer division, check-then-act races, leaked internal state.

## Layout

```
src/main/java/com/example/interview/
  OrderBook.java          1. collections + streams aggregation
  IntervalScheduler.java  2. merge intervals / meeting rooms
  GraphRoutes.java        3. BFS shortest path
  TextWindow.java         4. sliding window + frequency counts
  LruCache.java           5. LRU cache design
  RateLimiter.java        6. concurrency (fixed-window limiter)
  PaymentProcessor.java   7. sealed types + money
  Verify.java             the spec, as assertions — do not edit
solutions/ANSWERS.md      interviewer's key: every bug, why it bites, the fix
solutions/fixed/          reference fixes, each marked with a FIX comment
run.ps1                   compile + run the spec
```

**Verified on JDK 21.0.13:** the exercises compile clean under `javac -Xlint:all`, and
`Verify` reports **30 of 42 checks failing**. The reference fixes in `solutions/fixed`
compile just as clean and go **42/42 green**, so the kit is known to be solvable —
there are no unreachable assertions.

The javadoc on each method **is** the spec, and `Verify` only asserts what that
javadoc already promises. If a check looks unfair, that is itself a finding worth
saying out loud.

## Run it

Needs a JDK 21 or newer (`Thread.ofPlatform()`, pattern matching for `switch`).

```powershell
javac -d out (Get-ChildItem -Recurse src -Filter *.java | ForEach-Object FullName)
```

```powershell
java -cp out com.example.interview.Verify
```

Green run exits 0; otherwise it prints every failing check with the reason. Or just:

```powershell
.\run.ps1
```

To see the target state, compile `solutions/fixed/src` instead of `src`.

## How to run the interview

**Format (60 min, pick 3 exercises):**

| Phase | Time | What you are watching for |
| --- | --- | --- |
| Read one file cold, think aloud | 5 min | Do they build a model before touching code? Do they read the javadoc as the contract? |
| Predict failures *before* running `Verify` | 5 min | Can they spot a bug by reading, or only by bisecting output? |
| Fix until green | 20 min | Minimal targeted fixes, or rewrite-from-scratch panic? |
| Explain each fix + what else it breaks | 10 min | Can they name the mechanism (unboxing, scale, visibility) rather than "it just needed changing"? |

**Difficulty / what each one probes**

| # | Exercise | Difficulty | Probes |
| --- | --- | --- | --- |
| 1 | `OrderBook` | easy | Collectors, string identity, encapsulation, float money |
| 2 | `IntervalScheduler` | easy–medium | sort keys, boundary conditions, heap direction |
| 3 | `GraphRoutes` | medium | BFS vs DFS, visited sets, path reconstruction, level counting |
| 4 | `TextWindow` | medium | window invariants, charset assumptions, map ordering |
| 5 | `LruCache` | medium | API-contract reading, eviction policy, integer division |
| 6 | `RateLimiter` | hard | atomicity, publication, check-then-act, lock scope |
| 7 | `PaymentProcessor` | medium–hard | immutability, `BigDecimal` scale vs value, PII in logs |

**Strong signals**
- Reaches for the javadoc/spec before the debugger.
- Says "this will be wrong for X" and is right.
- Fixes the cause, not the assertion (and notices that editing `Verify` is cheating).
- On exercise 6, says the single-threaded checks can pass while the design is still
  broken, and reasons about *why* the race shows up rather than adding
  `synchronized` everywhere and hoping.
- Flags bugs `Verify` does **not** catch (there are several planted ones — see the key).

**Weak signals**
- Rewrites a whole class instead of locating the defect.
- Treats a passing suite as proof of correctness.
- Cannot explain `hits / (hits + misses)` returning `0.0`.
- "The AI wrote it, so it's probably fine."

## Variants

- **Pair-review mode:** no running allowed. Candidate reviews one file and lists bugs
  with severity. Then run `Verify` together and compare.
- **Write-the-test mode:** hand them a fixed file and ask for the regression test that
  would have caught it.
- **Code-review mode:** ask them to write the PR comments they'd leave on exercise 7.
