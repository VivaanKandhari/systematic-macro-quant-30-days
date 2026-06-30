"""
Day 1: Random Variables & Expected Value

Mini-project:
HSI Return Expectations Calculator

Research question:
What has the historical distribution of Hang Seng Index daily returns looked like,
and what is the average daily/annualized return?

Research summary:
This script treats daily HSI returns as observations of a random variable. It
estimates the average daily payoff, annualizes that average, measures how often
the index was positive or negative, and visualizes the return distribution.

Conclusion to look for:
If the mean daily return is small compared with the range of daily outcomes,
then expected return alone is not enough for investment decisions. A macro
investor also needs volatility, tail risk, and regime analysis.
"""

from pathlib import Path

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


TICKER = "^HSI"
PERIOD = "5y"
TRADING_DAYS = 252
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def get_price_series(ticker: str, period: str) -> pd.Series:
    data = yf.download(ticker, period=period, auto_adjust=True)
    prices = data["Close"]

    # yfinance may return a one-column DataFrame even for one ticker.
    if isinstance(prices, pd.DataFrame):
        prices = prices[ticker]

    return prices.dropna()


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    prices = get_price_series(TICKER, PERIOD)
    returns = prices.pct_change().dropna()

    mean_daily_return = returns.mean()
    median_daily_return = returns.median()
    annualized_return = (1 + mean_daily_return) ** TRADING_DAYS - 1
    positive_day_probability = (returns > 0).mean()
    negative_day_probability = (returns < 0).mean()

    summary = pd.DataFrame(
        {
            "Metric": [
                "Mean daily return",
                "Median daily return",
                "Annualized return",
                "Positive day probability",
                "Negative day probability",
                "Worst day",
                "Best day",
            ],
            "Value": [
                f"{mean_daily_return:.4%}",
                f"{median_daily_return:.4%}",
                f"{annualized_return:.2%}",
                f"{positive_day_probability:.2%}",
                f"{negative_day_probability:.2%}",
                f"{returns.min():.2%}",
                f"{returns.max():.2%}",
            ],
        }
    )

    print("\nHSI Return Expectations Calculator")
    print(summary.to_string(index=False))

    # Research interpretation:
    # The mean daily return estimates the center of the return distribution.
    # The positive/negative day probabilities show how often HSI rose or fell.
    # The worst and best days remind us that the distribution, not just the
    # average, matters for real portfolio risk.

    plt.figure(figsize=(12, 6))
    plt.hist(returns, bins=60, edgecolor="white", alpha=0.75)
    plt.axvline(
        mean_daily_return,
        color="red",
        linewidth=2,
        label=f"Mean daily return: {mean_daily_return:.4%}",
    )
    plt.title("Hang Seng Index Daily Return Distribution")
    plt.xlabel("Daily return")
    plt.ylabel("Number of trading days")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "hsi_return_histogram.png", dpi=150)
    plt.show()

    # Conclusion:
    # This chart should show most daily returns clustered near zero, with some
    # much larger positive and negative days. That is the first quant lesson:
    # returns are uncertain outcomes drawn from a distribution.


if __name__ == "__main__":
    main()
