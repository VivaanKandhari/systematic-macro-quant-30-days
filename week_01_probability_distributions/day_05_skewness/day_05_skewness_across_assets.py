"""
Day 5: Skewness & Asymmetric Returns

Mini-project:
Skewness Across Asset Classes

Research question:
Which major macro assets have the most negative or positive return asymmetry?

Research summary:
This script downloads five years of real market data, calculates daily returns,
then compares skewness, worst day, best day, mean return, and volatility across
equities, gold, bonds, the US dollar, and Bitcoin.

Conclusion to look for:
Negative skew means the left tail is worse than the right tail. For a macro
investor, this can reveal hidden crash risk that average return and volatility
do not fully describe.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from scipy.stats import skew


TICKERS = {
    "HSI": "^HSI",
    "Gold": "GLD",
    "Bonds": "TLT",
    "USD": "UUP",
    "Bitcoin": "BTC-USD",
}
PERIOD = "5y"
TRADING_DAYS = 252
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def print_clean_table(table: pd.DataFrame) -> None:
    """Print a compact ASCII table that stays readable in notebooks/terminals."""
    rows = [[str(value) for value in row] for row in table.to_numpy()]
    headers = [str(column) for column in table.columns]
    widths = [
        max(len(header), *(len(row[index]) for row in rows))
        for index, header in enumerate(headers)
    ]

    border = "+-" + "-+-".join("-" * width for width in widths) + "-+"
    header_row = "| " + " | ".join(
        header.ljust(width) for header, width in zip(headers, widths)
    ) + " |"

    print(border)
    print(header_row)
    print(border)

    for row in rows:
        print("| " + " | ".join(
            value.rjust(width) for value, width in zip(row, widths)
        ) + " |")

    print(border)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    data = yf.download(
        list(TICKERS.values()),
        period=PERIOD,
        auto_adjust=True,
        progress=False,
    )
    prices = data["Close"]

    reverse_names = {symbol: name for name, symbol in TICKERS.items()}
    prices = prices.rename(columns=reverse_names)
    returns = prices.pct_change(fill_method=None).dropna(how="all")

    rows = []

    for asset in TICKERS:
        r = returns[asset].dropna()

        rows.append(
            {
                "Asset": asset,
                "Mean Daily Return": r.mean(),
                "Daily Volatility": r.std(),
                "Annualized Vol": r.std() * (TRADING_DAYS ** 0.5),
                "Skewness": skew(r, bias=False),
                "Worst Day": r.min(),
                "Best Day": r.max(),
            }
        )

    results = pd.DataFrame(rows).sort_values("Skewness")

    display_results = pd.DataFrame(
        {
            "Asset": results["Asset"],
            "Mean": results["Mean Daily Return"].map(lambda x: f"{x:.3%}"),
            "Daily Vol": results["Daily Volatility"].map(lambda x: f"{x:.2%}"),
            "Ann. Vol": results["Annualized Vol"].map(lambda x: f"{x:.2%}"),
            "Skew": results["Skewness"].map(lambda x: f"{x:.2f}"),
            "Worst Day": results["Worst Day"].map(lambda x: f"{x:.2%}"),
            "Best Day": results["Best Day"].map(lambda x: f"{x:.2%}"),
        }
    )

    print("\nSkewness Across Asset Classes")
    print("(sorted from most negative skew to most positive skew)\n")
    print_clean_table(display_results)

    most_negative = results.iloc[0]
    most_positive = results.iloc[-1]

    print()
    print(
        f"Most negative skew: {most_negative['Asset']} "
        f"({most_negative['Skewness']:.2f}). "
        "Its downside tail was the most asymmetric in this sample."
    )
    print(
        f"Most positive skew: {most_positive['Asset']} "
        f"({most_positive['Skewness']:.2f}). "
        "Its upside tail was the most asymmetric in this sample."
    )

    # Research interpretation:
    # Kurtosis tells us whether extreme moves happen unusually often. Skewness
    # tells us whether those extreme moves lean more toward losses or gains.
    # Negative skew is especially important for portfolio survival because it
    # means rare bad days are larger than rare good days.

    fig, axes = plt.subplots(3, 2, figsize=(13, 10))
    axes = axes.flatten()

    for ax, asset in zip(axes, TICKERS):
        r = returns[asset].dropna()
        ax.hist(r, bins=60, alpha=0.75, edgecolor="white")
        ax.axvline(0, color="black", linestyle="--", linewidth=1)
        ax.set_title(asset)
        ax.set_xlabel("Daily return")
        ax.set_ylabel("Frequency")
        ax.grid(True, alpha=0.35)

    for ax in axes[len(TICKERS):]:
        ax.axis("off")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "asset_return_skewness_histograms.png", dpi=150)
    plt.show()

    # Conclusion:
    # A crisis-aware macro investor should not only ask which asset has the
    # highest return or volatility. The direction of the tail matters. Assets
    # with strongly negative skew can look acceptable most days, then deliver
    # unusually large losses when conditions break.


if __name__ == "__main__":
    main()
