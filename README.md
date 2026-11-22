# interview-bug-hunt

Technical interviews where the candidate is handed **working-looking, AI-written code
that is wrong**, plus a spec that fails, and has to find out why.

A substitute for LeetCode-style whiteboarding. Nobody invents an algorithm from scratch;
they do the thing the job actually is — read unfamiliar code, reconstruct what it was
meant to do, locate the defect, fix it, and explain the mechanism.

## What is here

| Kit | Exercises | Spec | Baseline |
| --- | --- | --- | --- |
| [python/](python/) | 50 NeetCode **Hard** problems | `verify.py`, 156 assertions | 77 checks fail, 50/50 problems broken |
| [java/](java/) | 7 engineering exercises (collections, money, concurrency) | `Verify.java`, 42 assertions | 30 checks fail |

Both are verified: the planted bugs really do fail, and the reference fixes really do go
green. No assertion is unreachable, and no exercise is accidentally correct.

- **[QUESTIONS.md](QUESTIONS.md)** — index of all 57, with LeetCode numbers, categories,
  bug classes, and a coverage table for picking a varied set.
- `*/solutions/ANSWERS.md` — interviewer's key: every bug, why it bites, the fix, and the
  bugs the spec deliberately does *not* catch.
- `*/solutions/fixed/` — working implementations, each change marked `FIX:`.

## Quick start

```powershell
cd python; python verify.py -q
```

```powershell
cd java; .\run.ps1
```

Python needs 3.9+ and nothing else. Java needs a JDK 21+.

## Running an interview

Each kit's README has the format, time-boxing, suggested problem sets, and the strong and
weak signals to watch for. In short:

1. Hand over **2–4 exercises**, not the whole kit.
2. Have them read one cold and think aloud *before* running anything.
3. Ask them to predict the failure, then run the spec.
4. Score the explanation, not just the green run — "the invariant was X and this line
   breaks it" is the signal; "I changed it and it passed" is not.

The docstrings and javadoc are the contract, and every assertion only checks what the
contract already promises. If a candidate argues a check is unfair, that is itself a
finding worth hearing out.

## Why this format

The bugs are not typos and the compiler catches none of them. They are the failure mode
of generated code on hard problems: the shape of the algorithm is right, the comments are
better than most production code, the happy path passes — and one invariant is quietly
violated. The wrong pointer advanced. `>=` where `>` was meant. State never restored. The
second thread. The last element.

Which is the skill worth hiring for now: not producing the solution, but being able to
tell whether the solution in front of you actually does what it claims.
