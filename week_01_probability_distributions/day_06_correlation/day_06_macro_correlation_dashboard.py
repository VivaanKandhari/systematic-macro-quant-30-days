"""
Day 6: Correlation - The Most Important Stat in Macro

Mini-project:
Macro Correlation Dashboard

Research question:
How do major macro assets move together, and does HSI's relationship with the
S&P 500 change during crisis periods?

Research summary:
This script downloads five years of real market data, converts all series into
daily percentage changes, builds a correlation matrix, saves a heatmap, and
plots the rolling 60-day correlation between HSI and S&P 500.

Conclusion to look for:
Correlation is a diversification map. Assets that look independent in normal
periods can become more correlated during market stress, reducing the protection
investors thought they had.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import yfinance as yf
from tabulate import tabulate


TICKERS = {
    "HSI": "^HSI",
    "S&P 500": "^GSPC",
    "US 10Y Yield": "^TNX",
    "Gold": "GLD",
    "USD/CNH": "USDCNH=X",
    "Oil": "CL=F",
}
PERIOD = "5y"
MIN_DATA_COVERAGE = 0.80
ROLLING_WINDOW = 60
COVID_START = pd.Timestamp("2020-02-01")
COVID_END = pd.Timestamp("2020-04-30")
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def print_section(title: str) -> None:
    line = "=" * 100
    print(f"\n{line}")
    print(title)
    print(f"{line}\n")


def print_table(table: pd.DataFrame, headers: str = "keys") -> None:
    print(tabulate(table, headers=headers, tablefmt="grid", showindex=False))


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    symbols = list(TICKERS.values())

    data = yf.download(
        symbols,
        period=PERIOD,
        auto_adjust=True,
        progress=False,
    )

    prices = data["Close"]

    reverse_names = {symbol: name for name, symbol in TICKERS.items()}
    prices = prices.rename(columns=reverse_names)

    prices = prices.dropna(axis=1, how="all")
    prices = prices.ffill()

    returns = prices.pct_change(fill_method=None)
    returns = returns.dropna(how="all")
    returns = returns.dropna(axis=1, thresh=int(len(returns) * MIN_DATA_COVERAGE))

    correlation_matrix = returns.corr()

    coverage_table = pd.DataFrame(
        {
            "Asset": returns.columns,
            "Usable Days": [returns[col].dropna().shape[0] for col in returns.columns],
            "Missing Days": [returns[col].isna().sum() for col in returns.columns],
            "Mean Daily Move": [returns[col].mean() for col in returns.columns],
            "Daily Vol": [returns[col].std() for col in returns.columns],
        }
    )
    coverage_display = coverage_table.copy()
    coverage_display["Mean Daily Move"] = coverage_display["Mean Daily Move"].map(
        lambda x: f"{x:.3%}"
    )
    coverage_display["Daily Vol"] = coverage_display["Daily Vol"].map(
        lambda x: f"{x:.2%}"
    )

    corr_display = correlation_matrix.round(2).reset_index()
    corr_display = corr_display.rename(columns={"index": "Asset"})

    print_section("MACRO CORRELATION DASHBOARD")
    print("Assets used:")
    print(", ".join(returns.columns))
    print(f"\nReturn matrix shape: {returns.shape[0]} trading days x {returns.shape[1]} assets")

    print_section("DATA COVERAGE")
    print_table(coverage_display)

    print_section("CORRELATION MATRIX")
    print_table(corr_display)

    if "HSI" in returns.columns and "S&P 500" in returns.columns:
        hsi_spx_corr = correlation_matrix.loc["HSI", "S&P 500"]
        print_section("KEY MACRO READ")
        print(f"HSI vs S&P 500 full-sample correlation: {hsi_spx_corr:.2f}")

        if hsi_spx_corr > 0.5:
            print("Interpretation: HSI and S&P 500 moved together strongly in this sample.")
        elif hsi_spx_corr > 0.2:
            print("Interpretation: HSI and S&P 500 had a moderate positive relationship.")
        elif hsi_spx_corr > -0.2:
            print("Interpretation: HSI and S&P 500 were weakly related over the full sample.")
        else:
            print("Interpretation: HSI and S&P 500 tended to move in opposite directions.")

    plt.figure(figsize=(10, 7))
    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        square=True,
        cbar_kws={"label": "Correlation"},
    )
    plt.title("Macro Asset Correlation Matrix")
    plt.tight_layout()
    heatmap_path = OUTPUT_DIR / "macro_asset_correlation_heatmap.png"
    plt.savefig(heatmap_path, dpi=150, bbox_inches="tight")
    print(f"\nChart saved: {heatmap_path}")
    plt.show()

    if "HSI" in returns.columns and "S&P 500" in returns.columns:
        rolling_corr = returns["HSI"].rolling(ROLLING_WINDOW).corr(returns["S&P 500"])

        plt.figure(figsize=(12, 6))
        plt.plot(
            rolling_corr,
            linewidth=2,
            label=f"{ROLLING_WINDOW}-day rolling correlation: HSI vs S&P 500",
        )
        plt.axvspan(
            COVID_START,
            COVID_END,
            color="red",
            alpha=0.2,
            label="COVID crash period",
        )
        plt.axhline(0, color="black", linewidth=1)
        plt.title("Rolling Correlation: HSI vs S&P 500")
        plt.xlabel("Date")
        plt.ylabel("Correlation")
        plt.legend()
        plt.grid(True, alpha=0.35)
        plt.tight_layout()
        rolling_path = OUTPUT_DIR / "hsi_sp500_rolling_correlation.png"
        plt.savefig(rolling_path, dpi=150, bbox_inches="tight")
        print(f"Chart saved: {rolling_path}")
        plt.show()
    else:
        print("\nCould not plot rolling correlation because HSI or S&P 500 is missing.")


if __name__ == "__main__":
    main()
