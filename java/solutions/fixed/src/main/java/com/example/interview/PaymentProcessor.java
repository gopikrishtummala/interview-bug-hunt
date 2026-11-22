package com.example.interview;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Arrays;
import java.util.Objects;

/** Reference fix. See solutions/ANSWERS.md, exercise 7. */
public final class PaymentProcessor {

    // FIX: string literals, so the rates are the decimals we wrote, not binary approximations.
    private static final BigDecimal CARD_RATE = new BigDecimal("0.029");
    private static final BigDecimal WALLET_RATE = new BigDecimal("0.01");
    private static final BigDecimal BANK_FEE = new BigDecimal("0.25");

    public sealed interface Payment permits Card, Bank, Wallet {}

    /** FIX: validate in a compact constructor instead of failing somewhere downstream. */
    public record Card(String number, BigDecimal amount) implements Payment {
        public Card {
            Objects.requireNonNull(number, "number");
            requireNonNegative(amount);
        }
    }

    public record Bank(String iban, BigDecimal amount) implements Payment {
        public Bank {
            Objects.requireNonNull(iban, "iban");
            requireNonNegative(amount);
        }
    }

    public record Wallet(String userId, BigDecimal amount) implements Payment {
        public Wallet {
            Objects.requireNonNull(userId, "userId");
            requireNonNegative(amount);
        }
    }

    private static void requireNonNegative(BigDecimal amount) {
        Objects.requireNonNull(amount, "amount");
        if (amount.signum() < 0) {
            throw new IllegalArgumentException("amount must not be negative: " + amount);
        }
    }

    /** FIX: signum() instead of equals() for zero, and every result rounded to cents. */
    public BigDecimal fee(Payment payment) {
        BigDecimal fee = switch (payment) {
            case Card card -> card.amount().multiply(CARD_RATE);
            case Bank bank -> bank.amount().signum() == 0 ? BigDecimal.ZERO : BANK_FEE;
            case Wallet wallet -> wallet.amount().multiply(WALLET_RATE);
        };
        return fee.setScale(2, RoundingMode.HALF_UP);
    }

    /** FIX: BigDecimal is immutable — keep the result of add(). */
    public BigDecimal total(Payment... payments) {
        return Arrays.stream(payments)
                .map(this::amountOf)
                .reduce(BigDecimal.ZERO, BigDecimal::add)
                .setScale(2, RoundingMode.HALF_UP);
    }

    /** FIX: compareTo compares value; equals also compares scale, so 10 != 10.00. */
    public boolean sameAmount(Payment a, Payment b) {
        return amountOf(a).compareTo(amountOf(b)) == 0;
    }

    /** FIX: never put a full PAN or IBAN in a log line. */
    public String describe(Payment payment) {
        return switch (payment) {
            case Card card -> "card " + mask(card.number()) + " amount " + card.amount();
            case Bank bank -> "bank " + mask(bank.iban()) + " amount " + bank.amount();
            case Wallet wallet -> "wallet " + mask(wallet.userId()) + " amount " + wallet.amount();
        };
    }

    private static String mask(String identifier) {
        if (identifier.length() <= 4) {
            return "****";
        }
        return "****" + identifier.substring(identifier.length() - 4);
    }

    private BigDecimal amountOf(Payment payment) {
        return switch (payment) {
            case Card card -> card.amount();
            case Bank bank -> bank.amount();
            case Wallet wallet -> wallet.amount();
        };
    }
}
