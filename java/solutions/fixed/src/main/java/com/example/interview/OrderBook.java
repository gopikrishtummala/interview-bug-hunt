package com.example.interview;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/** Reference fix. See solutions/ANSWERS.md, exercise 1. */
public final class OrderBook {

    public enum Side { BUY, SELL }

    public record Order(String id, String symbol, Side side, int quantity, double price) {}

    private final List<Order> orders = new ArrayList<>();

    public void add(Order order) {
        orders.add(order);
    }

    /** FIX: hand back a copy so callers cannot mutate the book. */
    public List<Order> orders() {
        return List.copyOf(orders);
    }

    /** FIX: a merge function, because a symbol legitimately has several orders. */
    public Map<String, Order> orderBySymbol() {
        return orders.stream()
                .collect(Collectors.toMap(Order::symbol, order -> order, (first, second) -> first));
    }

    /** FIX: equals() not ==, and BigDecimal all the way through instead of double. */
    public BigDecimal notional(String symbol) {
        BigDecimal total = BigDecimal.ZERO;
        for (Order order : orders) {
            if (order.symbol().equals(symbol)) {
                total = total.add(BigDecimal.valueOf(order.price())
                        .multiply(BigDecimal.valueOf(order.quantity())));
            }
        }
        return total.setScale(2, RoundingMode.HALF_UP);
    }

    /** FIX: a real double comparator, descending as documented. */
    public List<Order> topOrders(int n) {
        return orders.stream()
                .sorted(Comparator.comparingDouble(Order::price).reversed())
                .limit(n)
                .toList();
    }

    /** FIX: removeIf instead of mutating during iteration. */
    public void cancelAllFor(String symbol) {
        orders.removeIf(order -> symbol.equals(order.symbol()));
    }

    /** FIX: average in double, and an empty book is 0.0 rather than a divide by zero. */
    public double averageQuantity() {
        return orders.stream().mapToInt(Order::quantity).average().orElse(0.0);
    }

    /** FIX: compare the enums, not the strings their names happen to be interned as. */
    public boolean hasSide(Side side) {
        return orders.stream().anyMatch(order -> order.side() == side);
    }
}
