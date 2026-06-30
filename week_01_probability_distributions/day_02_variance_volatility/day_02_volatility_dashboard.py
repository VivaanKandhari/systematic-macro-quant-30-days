"""
Day 2: Variance, Volatility & Why They Matter

Mini-project:
Volatility Comparison Dashboard

Research question:
How volatile has HSI been compared with the S&P 500 and Nasdaq?

Research summary:
This script measures realized volatility for HSI, S&P 500, and Nasdaq using
historical daily returns. It annualizes daily volatility and plots rolling HSI
volatility to show how market risk changes through time.

Conclusion to look for:
Higher volatility means larger typical return swings. A systematic macro
investor would usually size positions smaller in higher-volatility markets if
targeting equal risk across assets.
"""

from pathlib import Path

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


TICKERS = {
    "HSI": "^HSI",
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
}
PERIOD = "5y"
TRADING_DAYS = 252
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    data = yf.download(list(TICKERS.values()), period=PERIOD, auto_adjust=True)
    prices = data["Close"]

    reverse_names = {symbol: name for name, symbol in TICKERS.items()}
    prices = prices.rename(columns=reverse_names)

    returns = prices.pct_change().dropna()

    daily_volatility = returns.std()
    annualized_volatility = daily_volatility * (TRADING_DAYS ** 0.5)

    vol_table = pd.DataFrame(
        {
            "Daily Volatility": daily_volatility,
            "Annualized Volatility": annualized_volatility,
        }
    )

    display_table = vol_table.copy()
    display_table["Daily Volatility"] = display_table["Daily Volatility"].map(
        lambda x: f"{x:.2%}"
    )
    display_table["Annualized Volatility"] = display_table[
        "Annualized Volatility"
    ].map(lambda x: f"{x:.2%}")

    print("\nVolatility Comparison Dashboard")
    print(display_table.to_string())

    # Research interpretation:
    # Annualized volatility converts daily return instability into the yearly
    # risk language used by portfolio managers. Comparing HSI, S&P 500, and
    # Nasdaq shows that equal dollar allocations are not equal-risk allocations.

    hsi_vol = annualized_volatility["HSI"]
    sp500_vol = annualized_volatility["S&P 500"]
    difference = hsi_vol / sp500_vol - 1

    if difference > 0:
        print(f"\nHSI is {difference:.2%} more volatile than the S&P 500.")
    else:
        print(f"\nHSI is {abs(difference):.2%} less volatile than the S&P 500.")

    rolling_hsi_vol = returns["HSI"].rolling(30).std() * (TRADING_DAYS ** 0.5)

    plt.figure(figsize=(12, 6))
    plt.plot(rolling_hsi_vol, label="HSI 30-day rolling annualized volatility")
    plt.axvspan(
        pd.Timestamp("2020-02-01"),
        pd.Timestamp("2020-04-30"),
        color="red",
        alpha=0.2,
        label="COVID crash period",
    )
    plt.title("HSI Rolling 30-Day Annualized Volatility")
    plt.xlabel("Date")
    plt.ylabel("Annualized volatility")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "hsi_rolling_volatility.png", dpi=150)
    plt.show()

    # Conclusion:
    # Rolling volatility should spike during crisis periods because investors
    # reduce risk, liquidity falls, and prices move more violently. Volatility is
    # therefore both a risk measure and a practical input for position sizing.


if __name__ == "__main__":
    main()
