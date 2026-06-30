"""
Day 3: Normal Distribution & Market Tail Risk

Mini-project:
HSI Risk Probability Calculator

Research question:
Does a fitted normal distribution underestimate Hang Seng Index tail risk?

Research summary:
This script fits a normal distribution to HSI daily returns using the historical
mean and standard deviation. It compares normal-model probabilities against
actual historical frequencies for large loss/gain thresholds.

Conclusion to look for:
The normal distribution can be a useful baseline near the center of the return
distribution, but it often underestimates extreme market moves. If historical
tail probabilities are higher than normal-model probabilities, HSI returns show
fat-tail behavior.
"""

from pathlib import Path

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


TICKER = "^HSI"
PERIOD = "5y"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def get_price_series(ticker: str, period: str) -> pd.Series:
    data = yf.download(ticker, period=period, auto_adjust=True)
    prices = data["Close"]

    # yfinance may return a one-column DataFrame even for one ticker.
    if isinstance(prices, pd.DataFrame):
        prices = prices[ticker]

    return prices.dropna()


def tail_probability(returns: pd.Series, threshold: float, mean: float, std: float) -> tuple[float, float, float]:
    z_score = (threshold - mean) / std

    if threshold < mean:
        normal_probability = norm.cdf(z_score)
        historical_probability = (returns < threshold).mean()
    else:
        normal_probability = 1 - norm.cdf(z_score)
        historical_probability = (returns > threshold).mean()

    return z_score, normal_probability, historical_probability


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    prices = get_price_series(TICKER, PERIOD)
    returns = prices.pct_change().dropna()

    mean = returns.mean()
    std = returns.std()

    thresholds = {
        "P(return < -1%)": -0.01,
        "P(return < -3%)": -0.03,
        "P(return > +5%)": 0.05,
    }

    print("\nHSI Risk Probability Calculator")
    print(f"Mean daily return: {mean:.4%}")
    print(f"Daily volatility: {std:.2%}")

    rows = []
    for label, threshold in thresholds.items():
        z_score, normal_probability, historical_probability = tail_probability(
            returns, threshold, mean, std
        )
        rows.append(
            {
                "Event": label,
                "Threshold": f"{threshold:.2%}",
                "Z-score": f"{z_score:.2f}",
                "Normal Probability": f"{normal_probability:.2%}",
                "Historical Probability": f"{historical_probability:.2%}",
            }
        )

    probability_table = pd.DataFrame(rows)
    print()
    print(probability_table.to_string(index=False))

    # Research interpretation:
    # Normal probability is what the bell-curve model predicts.
    # Historical probability is what actually happened in the data.
    # If historical downside events are more common than the normal model says,
    # then a naive normal risk model is underestimating crash risk.

    x = np.linspace(returns.min(), returns.max(), 500)
    normal_curve = norm.pdf(x, mean, std)

    plt.figure(figsize=(12, 6))
    plt.hist(
        returns,
        bins=60,
        density=True,
        alpha=0.65,
        edgecolor="white",
        label="Actual HSI returns",
    )
    plt.plot(
        x,
        normal_curve,
        color="red",
        linewidth=2,
        label="Fitted normal distribution",
    )
    plt.axvline(-0.03, color="black", linestyle="--", label="-3% loss threshold")
    plt.title("HSI Daily Returns vs Normal Distribution")
    plt.xlabel("Daily return")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "hsi_normal_distribution_fit.png", dpi=150)
    plt.show()

    # Conclusion:
    # The fitted normal curve is a benchmark, not proof that returns are normal.
    # A common market pattern is a sharp center plus heavier tails than the red
    # bell curve predicts. That failure motivates Day 4: fat tails.


if __name__ == "__main__":
    main()
