package com.example.interview;

import java.math.BigDecimal;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.concurrent.Callable;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

import com.example.interview.IntervalScheduler.Interval;
import com.example.interview.OrderBook.Order;
import com.example.interview.OrderBook.Side;
import com.example.interview.PaymentProcessor.Bank;
import com.example.interview.PaymentProcessor.Card;
import com.example.interview.PaymentProcessor.Wallet;

/**
 * The spec, expressed as assertions. Do not change this file during the interview:
 * every check here states behaviour the exercise's own javadoc already promises.
 */
public final class Verify {

    private static int passed;
    private static final List<String> FAILURES = new ArrayList<>();
    private static String section = "";

    public static void main(String[] args) {
        exercise1OrderBook();
        exercise2Intervals();
        exercise3Graph();
        exercise4Text();
        exercise5Cache();
        exercise6RateLimiter();
        exercise7Payments();

        System.out.println();
        System.out.println("passed: " + passed + "   failed: " + FAILURES.size());
        if (!FAILURES.isEmpty()) {
            System.out.println();
            System.out.println("Still failing:");
            FAILURES.forEach(failure -> System.out.println("  - " + failure));
            System.exit(1);
        }
        System.out.println("All green. Now walk through each fix and why it matters.");
    }

    // ---------------------------------------------------------------- exercise 1

    private static OrderBook sampleBook() {
        OrderBook book = new OrderBook();
        book.add(new Order("A", "AAPL", Side.BUY, 10, 150.0));
        book.add(new Order("B", "AAPL", Side.SELL, 5, 155.0));
        book.add(new Order("C", "MSFT", Side.BUY, 4, 400.0));
        return book;
    }

    private static void exercise1OrderBook() {
        section("1. OrderBook");

        check("orderBySymbol() survives two orders on one symbol",
                () -> sampleBook().orderBySymbol().keySet().equals(Set.of("AAPL", "MSFT")));

        check("notional(AAPL) is 2275.00",
                () -> sampleBook().notional("AAPL").compareTo(new BigDecimal("2275.00")) == 0);

        check("notional() works for a symbol built at runtime",
                () -> sampleBook().notional(new String("AAPL"))
                        .compareTo(new BigDecimal("2275.00")) == 0);

        check("topOrders(2) returns the two priciest, priciest first", () -> {
            List<Order> top = sampleBook().topOrders(2);
            return top.size() == 2 && top.get(0).id().equals("C") && top.get(1).id().equals("B");
        });

        check("cancelAllFor(AAPL) leaves one order", () -> {
            OrderBook book = sampleBook();
            book.cancelAllFor("AAPL");
            return book.orders().size() == 1;
        });

        check("averageQuantity() is 19/3, not 6", () -> {
            double average = sampleBook().averageQuantity();
            return Math.abs(average - (19.0 / 3.0)) < 1e-9;
        });

        check("orders() does not hand out the internal list", () -> {
            OrderBook book = sampleBook();
            try {
                book.orders().add(new Order("X", "TSLA", Side.BUY, 1, 1.0));
            } catch (UnsupportedOperationException expected) {
                return true;
            }
            return book.orders().size() == 3;
        });
    }

    // ---------------------------------------------------------------- exercise 2

    private static void exercise2Intervals() {
        section("2. IntervalScheduler");

        check("merge() joins overlaps and keeps the tail", () -> {
            List<Interval> merged = IntervalScheduler.merge(List.of(
                    new Interval(1, 3), new Interval(2, 6),
                    new Interval(8, 10), new Interval(15, 18)));
            return merged.equals(List.of(
                    new Interval(1, 6), new Interval(8, 10), new Interval(15, 18)));
        });

        check("merge() joins touching intervals", () -> IntervalScheduler
                .merge(List.of(new Interval(1, 3), new Interval(3, 5)))
                .equals(List.of(new Interval(1, 5))));

        check("merge() is not fooled by input order", () -> IntervalScheduler
                .merge(List.of(new Interval(5, 7), new Interval(1, 100), new Interval(2, 3)))
                .equals(List.of(new Interval(1, 100))));

        check("minRooms() is 2 for the classic case",
                () -> IntervalScheduler.minRooms(List.of(
                        new Interval(0, 30), new Interval(5, 10), new Interval(15, 20))) == 2);

        check("minRooms() is 1 for back-to-back meetings",
                () -> IntervalScheduler.minRooms(List.of(
                        new Interval(0, 10), new Interval(10, 20), new Interval(20, 30))) == 1);

        check("canAttendAll() is true when nothing overlaps",
                () -> IntervalScheduler.canAttendAll(
                        List.of(new Interval(1, 3), new Interval(3, 5), new Interval(9, 10))));

        check("canAttendAll() is false on a real clash",
                () -> !IntervalScheduler.canAttendAll(
                        List.of(new Interval(1, 4), new Interval(3, 5))));
    }

    // ---------------------------------------------------------------- exercise 3

    private static GraphRoutes sampleGraph() {
        GraphRoutes graph = new GraphRoutes();
        graph.addEdge("A", "B");
        graph.addEdge("B", "C");
        graph.addEdge("C", "D");
        graph.addEdge("A", "E");
        graph.addEdge("E", "D");
        return graph;
    }

    private static void exercise3Graph() {
        section("3. GraphRoutes");

        check("shortestPath(A, D) is the three-node route A-E-D",
                () -> sampleGraph().shortestPath("A", "D").equals(List.of("A", "E", "D")));

        check("shortestPath(A, A) is just [A]",
                () -> sampleGraph().shortestPath("A", "A").equals(List.of("A")));

        check("shortestPath() to an unknown node is empty",
                () -> sampleGraph().shortestPath("A", "Z").isEmpty());

        check("reachableWithin(A, 1) is {B, E}",
                () -> sampleGraph().reachableWithin("A", 1).equals(Set.of("B", "E")));

        check("reachableWithin(A, 2) is {B, C, D, E}",
                () -> sampleGraph().reachableWithin("A", 2).equals(Set.of("B", "C", "D", "E")));
    }

    // ---------------------------------------------------------------- exercise 4

    private static void exercise4Text() {
        section("4. TextWindow");

        check("longestUnique(abcabcbb) is 3", () -> TextWindow.longestUnique("abcabcbb") == 3);
        check("longestUnique(bbbbb) is 1", () -> TextWindow.longestUnique("bbbbb") == 1);
        check("longestUnique(pwwkew) is 3", () -> TextWindow.longestUnique("pwwkew") == 3);
        check("longestUnique(empty) is 0", () -> TextWindow.longestUnique("") == 0);

        check("isAnagram ignores case and spaces",
                () -> TextWindow.isAnagram("Astronomer", "Moon starer"));
        check("isAnagram(rat, car) is false", () -> !TextWindow.isAnagram("rat", "car"));

        check("firstUnique(swiss) is w",
                () -> TextWindow.firstUnique("swiss").equals(Optional.of('w')));
        check("firstUnique(loveleetcode) is v, in input order",
                () -> TextWindow.firstUnique("loveleetcode").equals(Optional.of('v')));
        check("firstUnique(aabb) is empty", () -> TextWindow.firstUnique("aabb").isEmpty());

        check("reverseWords collapses double spaces and keeps every word",
                () -> TextWindow.reverseWords("the sky  is blue").equals("blue is sky the"));
    }

    // ---------------------------------------------------------------- exercise 5

    private static void exercise5Cache() {
        section("5. LruCache");

        LruCache<String, Integer> cache = new LruCache<>(2);
        cache.put("a", 1);
        cache.put("b", 2);
        cache.get("a");
        cache.put("c", 3);

        check("the cache never grows past its capacity", () -> cache.size() == 2);
        check("the recently read entry survives", () -> cache.containsKey("a"));
        check("the least recently used entry is evicted", () -> !cache.containsKey("b"));
        check("the new entry is present", () -> cache.containsKey("c"));

        check("hitRate() reports a fraction", () -> {
            cache.get("missing");
            return Math.abs(cache.hitRate() - 0.5) < 1e-9;
        });
    }

    // ---------------------------------------------------------------- exercise 6

    private static void exercise6RateLimiter() {
        section("6. RateLimiter");

        check("only three of five calls are granted", () -> {
            RateLimiter limiter = new RateLimiter(3, Duration.ofMinutes(1));
            int granted = 0;
            for (int i = 0; i < 5; i++) {
                if (limiter.tryAcquire("user-1")) {
                    granted++;
                }
            }
            return granted == 3;
        });

        check("used() on an unknown key is 0",
                () -> new RateLimiter(3, Duration.ofMinutes(1)).used("nobody") == 0);

        check("1000 permits are handed out exactly once under contention", () -> {
            RateLimiter limiter = new RateLimiter(1000, Duration.ofMinutes(1));
            AtomicInteger granted = new AtomicInteger();
            int threads = 8;
            CountDownLatch start = new CountDownLatch(1);
            CountDownLatch done = new CountDownLatch(threads);
            for (int t = 0; t < threads; t++) {
                Thread.ofPlatform().start(() -> {
                    try {
                        start.await();
                        for (int i = 0; i < 400; i++) {
                            if (limiter.tryAcquire("shared")) {
                                granted.incrementAndGet();
                            }
                        }
                    } catch (Throwable ignored) {
                        // a corrupted map shows up as a wrong count below
                    } finally {
                        done.countDown();
                    }
                });
            }
            start.countDown();
            done.await();
            return granted.get() == 1000;
        });
    }

    // ---------------------------------------------------------------- exercise 7

    private static void exercise7Payments() {
        section("7. PaymentProcessor");

        PaymentProcessor processor = new PaymentProcessor();

        check("card fee on 100.00 is exactly 2.90",
                () -> processor.fee(new Card("4111111111111111", new BigDecimal("100.00")))
                        .compareTo(new BigDecimal("2.90")) == 0);

        check("a zero bank transfer costs nothing",
                () -> processor.fee(new Bank("DE02", new BigDecimal("0.00")))
                        .compareTo(BigDecimal.ZERO) == 0);

        check("total() adds the payments up",
                () -> processor.total(
                                new Card("4111111111111111", new BigDecimal("10.00")),
                                new Wallet("u1", new BigDecimal("5.50")))
                        .compareTo(new BigDecimal("15.50")) == 0);

        check("sameAmount() compares value, not scale",
                () -> processor.sameAmount(
                        new Card("4111111111111111", new BigDecimal("10")),
                        new Wallet("u1", new BigDecimal("10.00"))));

        check("describe() does not leak the card number",
                () -> !processor.describe(new Card("4111111111111111", new BigDecimal("1.00")))
                        .contains("4111111111111111"));
    }

    // ---------------------------------------------------------------- plumbing

    private static void section(String name) {
        section = name;
        System.out.println();
        System.out.println("== " + name + " ==");
    }

    private static void check(String name, Callable<Boolean> body) {
        try {
            if (Boolean.TRUE.equals(body.call())) {
                passed++;
                System.out.println("  pass  " + name);
                return;
            }
            recordFailure(name, "assertion was false");
        } catch (Throwable t) {
            recordFailure(name, t.getClass().getSimpleName()
                    + (t.getMessage() == null ? "" : ": " + t.getMessage()));
        }
    }

    private static void recordFailure(String name, String why) {
        FAILURES.add(section + " / " + name + "  ->  " + why);
        System.out.println("  FAIL  " + name + "  ->  " + why);
    }

    private Verify() {}
}
