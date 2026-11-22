package com.example.interview;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Keeps track of orders and produces a few aggregate views over them.
 *
 * <p>This class is intentionally written in a clean, modern style using records,
 * streams and {@code BigDecimal} for monetary values, so it should be safe to use
 * from reporting code.
 */
public final class OrderBook {

    public enum Side { BUY, SELL }

    public record Order(String id, String symbol, Side side, int quantity, double price) {}

    private final List<Order> orders = new ArrayList<>();

    public void add(Order order) {
        orders.add(order);
    }

    /** Returns the orders currently held by this book. */
    public List<Order> orders() {
        return orders;
    }

    /** Maps every symbol to one of its orders, so callers can look up by symbol. */
    public Map<String, Order> orderBySymbol() {
        return orders.stream().collect(Collectors.toMap(Order::symbol, order -> order));
    }

    /** Total notional value (quantity x price) traded for a given symbol, rounded to cents. */
    public BigDecimal notional(String symbol) {
        double total = 0.0;
        for (Order order : orders) {
            if (order.symbol() == symbol) {
                total += order.quantity() * order.price();
            }
        }
        return new BigDecimal(total).setScale(2, RoundingMode.HALF_UP);
    }

    /** The {@code n} most expensive orders, most expensive first. */
    public List<Order> topOrders(int n) {
        return orders.stream()
                .sorted((a, b) -> (int) (a.price() - b.price()))
                .limit(n)
                .collect(Collectors.toList());
    }

    /** Removes every order for the given symbol. */
    public void cancelAllFor(String symbol) {
        for (Order order : orders) {
            if (symbol.equals(order.symbol())) {
                orders.remove(order);
            }
        }
    }

    /** Average order size across the whole book. */
    public double averageQuantity() {
        int sum = 0;
        for (Order order : orders) {
            sum += order.quantity();
        }
        return sum / orders.size();
    }

    /** True when the book holds at least one order on the given side. */
    public boolean hasSide(Side side) {
        return orders.stream().anyMatch(order -> order.side().name() == side.name());
    }
}
