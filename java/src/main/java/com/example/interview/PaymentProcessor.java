package com.example.interview;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Objects;

/**
 * Fees and totals over a sealed hierarchy of payment methods.
 * All amounts are in the same currency and all results are rounded to cents.
 */
public final class PaymentProcessor {

    public sealed interface Payment permits Card, Bank, Wallet {}

    public record Card(String number, BigDecimal amount) implements Payment {}

    public record Bank(String iban, BigDecimal amount) implements Payment {}

    public record Wallet(String userId, BigDecimal amount) implements Payment {}

    /** Processing fee: 2.9% for cards, a flat 0.25 for bank transfers, 1% for wallets. */
    public BigDecimal fee(Payment payment) {
        return switch (payment) {
            case Card card -> card.amount().multiply(new BigDecimal(0.029));
            case Bank bank -> bank.amount().equals(BigDecimal.ZERO)
                    ? BigDecimal.ZERO
                    : new BigDecimal("0.25");
            case Wallet wallet -> wallet.amount().multiply(new BigDecimal("0.01"));
        };
    }

    /** Sum of every payment's amount, rounded to cents. */
    public BigDecimal total(Payment... payments) {
        BigDecimal total = BigDecimal.ZERO;
        for (Payment payment : payments) {
            total.add(amountOf(payment));
        }
        return total.setScale(2, RoundingMode.HALF_UP);
    }

    /** True when both payments move the same amount of money. */
    public boolean sameAmount(Payment a, Payment b) {
        return Objects.equals(amountOf(a), amountOf(b));
    }

    /** A short, log-safe description of the payment. */
    public String describe(Payment payment) {
        if (payment instanceof Card card) {
            return "card " + card.number() + " amount " + card.amount();
        }
        if (payment instanceof Bank bank) {
            return "bank " + bank.iban() + " amount " + bank.amount();
        }
        return payment.toString();
    }

    private BigDecimal amountOf(Payment payment) {
        return switch (payment) {
            case Card card -> card.amount();
            case Bank bank -> bank.amount();
            case Wallet wallet -> wallet.amount();
        };
    }
}
