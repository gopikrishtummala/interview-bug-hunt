# Interviewer's key

Do not hand this to the candidate.

Each entry is `bug → why it bites → fix`. **(V)** means `Verify` catches it.
**(latent)** means it does *not* — a candidate who finds those unprompted is strong,
and they are the best follow-up questions when someone goes green too fast.

Baseline on JDK 21: **30 of 42 checks fail**. Working reference fixes are in
`solutions/fixed/` (each change carries a `FIX:` comment) and run 42/42 green.

Two accidental passes worth knowing about, because a candidate may notice them:
`notional("AAPL")` passes with a literal and only fails for a runtime-built string
(interning), and `firstUnique("swiss")` happens to return the right answer because
HashMap's bucket order coincides with input order there — `"loveleetcode"` is the
check that actually exposes it. Both are good teaching moments: a passing test is not
the same as correct code.

---

## 1. OrderBook — 8 bugs

1. **(V)** `orders()` returns the internal `ArrayList`. Any caller can mutate the book,
   and `cancelAllFor` becomes unpredictable. → `return List.copyOf(orders);`
2. **(V)** `Collectors.toMap(Order::symbol, o -> o)` with two AAPL orders throws
   `IllegalStateException: Duplicate key`. The javadoc says "one of its orders", so a
   merge function is correct. → `toMap(Order::symbol, o -> o, (a, b) -> a)`, or
   `groupingBy` if the real intent was a list per symbol.
3. **(V)** `order.symbol() == symbol` compares references. It passes with literals
   (constant pool interning) and fails for a symbol read from a file or built at
   runtime — the nastiest class of bug, because it works in the demo. → `.equals()`.
4. **(latent)** Money in `double`, then `new BigDecimal(double)`. The sample numbers
   happen to be exact, so the suite passes; `0.1 + 0.2` style inputs will not. Also
   `new BigDecimal(0.1)` captures the full binary error, unlike
   `BigDecimal.valueOf(0.1)`. → make `Order.price` a `BigDecimal`; never use the
   `double` constructor.
5. **(V)** `(int) (a.price() - b.price())` truncates differences below 1.0 to `0`
   (so near-equal prices sort arbitrarily) and can overflow; and it sorts *ascending*
   while the javadoc promises priciest first.
   → `Comparator.comparingDouble(Order::price).reversed()`.
6. **(V)** `orders.remove(order)` inside a for-each → `ConcurrentModificationException`.
   → `orders.removeIf(o -> symbol.equals(o.symbol()))`.
7. **(V)** `averageQuantity` sums into an `int` and divides by an `int`, so `19/3`
   becomes `6` before being widened to `6.0`. Empty book → `ArithmeticException`.
   → `orders.stream().mapToInt(Order::quantity).average().orElse(0.0)`.
8. **(latent)** `order.side().name() == side.name()` compares `String`s by reference.
   It works only because `Enum.name()` hands back the same instance every time —
   accidental correctness. → compare the enums: `order.side() == side`.

---

## 2. IntervalScheduler — 6 bugs

1. **(V)** `merge` sorts by `end` instead of `start`. The whole sweep assumes
   start-order. → `Comparator.comparingInt(Interval::start)`.
2. **(V)** `next.start() < current.end()` does not join touching intervals, which the
   javadoc explicitly requires for coverage merging. → `<=`.
3. **(V)** The last `current` is never added — the final interval silently vanishes.
   → `merged.add(current);` after the loop.
4. **(V)** `minRooms` uses `PriorityQueue<>(Comparator.reverseOrder())`, a *max*-heap,
   so it inspects the latest-ending room and never reuses the one that frees up first.
   → natural ordering (min-heap).
5. **(V)** `canAttendAll` starts the inner loop at `j = i`, so every meeting is compared
   with itself and the answer is always `false`. → `j = i + 1`; better, sort by start
   and compare neighbours for O(n log n) instead of O(n²).
6. **(V)** `overlaps` uses `<=` on half-open bounds, so `[1,3)` and `[3,5)` "overlap".
   → `a.start() < b.end() && b.start() < a.end()`.

**(latent)** `merge` returns an immutable `List.of()` on one path and a mutable
`ArrayList` on the other — inconsistent contract. Ask about negative-width intervals
(`new Interval(5, 2)`) too: nothing rejects them.

---

## 3. GraphRoutes — 7 bugs

1. **(V)** `frontier.push(...)` + `frontier.pop()` is LIFO. This is a depth-first
   search wearing a BFS variable name, so the path it finds is not shortest.
   → `frontier.addLast(...)` / `frontier.pollFirst()`.
2. **(V)** `visited` is only marked on *pop*, and `parent` is overwritten each time a
   node is rediscovered. Even after fixing the queue order, parents point at the wrong
   predecessor. → mark visited and set `parent` at *enqueue* time, once per node.
3. **(V)** The path is reconstructed goal → start and never reversed.
   → `Collections.reverse(path)`, or build it with `LinkedList.addFirst`.
4. **(V)** An unreachable goal returns `[goal]`, because reconstruction starts at
   `goal` unconditionally. → return `List.of()` unless `goal.equals(start)` or
   `parent.containsKey(goal)`.
5. **(V)** `reachableWithin` increments `hops` once per *node* dequeued instead of once
   per *level*, so the limit means "look at maxHops+1 nodes". → capture
   `int levelSize = queue.size()` and drain exactly that many per hop.
6. **(V)** `seen.add(start)` contradicts the javadoc, which excludes the start node.
   → drop it (and guard against re-adding `start` via a cycle).
7. **(latent)** `addEdge` happily stores duplicate parallel edges and self-loops, and
   null-checks nothing; repeated calls bloat the adjacency lists and slow every query.

---

## 4. TextWindow — 7 bugs

1. **(V)** `longestUnique` shrinks the window by exactly one on a duplicate instead of
   looping until the duplicate is gone. The set and the `[left, right]` range fall out
   of sync — `"pwwkew"` and `"abba"` both break.
   → `while (window.contains(c)) { window.remove(s.charAt(left++)); }`
2. **(V)** `best = Math.max(best, right - left)` is off by one; the window
   `[left, right]` holds `right - left + 1` characters.
3. **(V)** `counts[c - 'a']` throws `ArrayIndexOutOfBoundsException` on the space in
   `"Moon starer"` — and on any digit, punctuation or accented letter. The javadoc
   says whitespace is ignored. → filter to letters, or count code points in a `Map`.
4. **(latent)** `toLowerCase()` without a locale. Under a Turkish default locale
   `"I".toLowerCase()` is `"ı"`, so the ASCII assumption breaks in production and not
   on your laptop. → `toLowerCase(Locale.ROOT)`.
5. **(V)** `firstUnique` iterates `HashMap.entrySet()`, whose order is hash order, not
   input order: `"swiss"` yields `'i'`. → `LinkedHashMap`, or re-scan the string and
   look each character up.
6. **(latent)** Everything here is `char`-based, so anything outside the BMP (emoji,
   some CJK) is processed as two surrogate halves. → `codePoints()`.
7. **(V)** `reverseWords`: `split(" ")` yields an empty token for the double space,
   `i > 0` drops the first word, and every line gets a trailing space.
   → `split("\\s+")`, `i >= 0`, and `String.join(" ", ...)` to avoid the dangling
   separator.

---

## 5. LruCache — 6 bugs

1. **(V)** `new LinkedHashMap<>(16, 0.75f, false)` — `accessOrder` is `false`, so this
   is a **FIFO** cache. Reads never refresh recency, which is the entire point. → `true`.
2. **(V)** `removeEldestEntry` returns `size() > capacity + 1`, so the cache holds one
   entry more than it promises. → `size() > capacity`.
3. **(V)** `hits / (hits + misses)` is integer division: the result is `0.0` until the
   hit rate reaches 100%, and `ArithmeticException` when no `get` has happened yet.
   → `(double) hits / total`, with a `total == 0` guard.
4. **(V)** `get` and `containsKey` treat `null` as "absent", so a cached `null` is
   invisible and every probe for it counts as a miss. → use
   `entries.containsKey(key)`, and reject `null` values in `put`.
5. **(latent)** Not thread-safe, and worse than it looks: `get` *mutates* (hit counters
   plus access-order relinking), so even an all-reads workload corrupts the linked
   list. → wrap in `Collections.synchronizedMap`, or use Caffeine.
6. **(latent)** `containsKey` does not count as a use while `get` does, so a caller who
   probes before reading quietly changes what gets evicted.

---

## 6. RateLimiter — 7 bugs (the hard one)

1. **(V, contention check)** A plain `HashMap` shared across threads. Concurrent `put`
   during a resize can lose entries or, historically, spin forever.
   → `ConcurrentHashMap`.
2. **(V)** `get` then `put` is check-then-act: two threads both see `null` and each
   creates a `Window`, so one thread's permits are simply forgotten.
   → `windows.computeIfAbsent(key, k -> new Window())`.
3. **(V)** `window.count++` is a read-modify-write on a non-volatile `int`. Permits are
   over-issued, and the `count < maxRequests` test is itself check-then-act.
   → do the whole decision atomically: `windows.compute(key, ...)`, a per-key lock, or
   `AtomicLong` packing the window start and the count into one value.
4. **(latent)** `windows` is non-final and reassigned by `reset()`. `reset()` is the
   only `synchronized` member, which synchronizes nothing useful — readers never
   acquire the same lock, so there is no safe publication of the new map. Classic
   half-lock. Ask: *what does this `synchronized` actually buy you?* (Nothing.)
5. **(latent)** `now - start > windowMillis` should be `>=`, and
   `System.currentTimeMillis()` is wall-clock: an NTP correction or DST-adjacent clock
   step can freeze the limiter or hand out a free window. → monotonic
   `System.nanoTime()`.
6. **(V)** `used()` dereferences the result of `windows.get(key)` without a null check,
   so it throws for any unknown key — against its own javadoc.
7. **(latent)** `acquire()` busy-spins; `Thread.sleep(0)` is not a yield point you can
   rely on and burns a core at the limit. → sleep until the window rolls over, or
   expose a `Semaphore`.

**Discussion to push for:** the single-threaded checks pass on the broken version.
Ask what test *would* have caught this before production, and whether they'd write
the limiter at all or reach for Guava's `RateLimiter` / Bucket4j / a Redis counter.

---

## 7. PaymentProcessor — 7 bugs

1. **(V)** `new BigDecimal(0.029)` is `0.0289999999999999993671...`, and the product is
   never rounded, so a 100.00 card payment yields `2.8999999...`.
   → `new BigDecimal("0.029")` and `setScale(2, RoundingMode.HALF_UP)`. Good follow-up:
   `HALF_UP` or `HALF_EVEN`, and who decides?
2. **(V)** `bank.amount().equals(BigDecimal.ZERO)` is `false` for `0.00`:
   `BigDecimal.equals` compares *scale as well as value*. A zero transfer gets charged
   0.25. → `compareTo(BigDecimal.ZERO) == 0`, or `signum() == 0`.
3. **(V)** `total.add(amountOf(payment));` throws the result away — `BigDecimal` is
   immutable, and the compiler says nothing. `total()` always returns `0.00`.
   → `total = total.add(...)`, or `Arrays.stream(payments).map(this::amountOf)
   .reduce(BigDecimal.ZERO, BigDecimal::add)`.
4. **(V)** `Objects.equals` on `BigDecimal` again: `10` and `10.00` are the same money
   and different objects. → `amountOf(a).compareTo(amountOf(b)) == 0`, null-handled.
5. **(V)** `describe()` puts the full card number — a PAN — into something explicitly
   documented as log-safe. → last four only: `"card ****" + number.substring(number.length() - 4)`.
   Note it also falls through to `Wallet.toString()`, which prints the user id.
6. **(latent)** Nothing validates the amounts: `new Card(null, null)` is constructible
   and NPEs later; negative amounts become negative fees. → compact constructor with
   `Objects.requireNonNull` and a `signum() >= 0` check.
7. **(latent)** No currency anywhere, so `total()` silently adds EUR to USD; and the
   wallet fee is unrounded like the card one.

---

## The through-line to say out loud at the end

Every one of these is a bug that *reads as correct*. None is a typo, none is caught by
the compiler, several pass a happy-path test. That is exactly the failure mode of
generated code: fluent, idiomatic, confidently wrong at the boundary — duplicate keys,
empty inputs, scale, locale, the second thread, the last element.

The skill being tested is not "can you invent an algorithm". It is "can you be the
reason this does not reach production".
