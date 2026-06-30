# Day 4: Fat Tails & Why Normal Distribution Fails Markets
# Mini-project: Fat Tail Detector
#
# Research question:
# Do HSI and S&P 500 daily returns produce more 3-sigma events than a normal
# distribution predicts?
#
# Summary:
# This program compares actual extreme return days against the number of
# extreme days predicted by a fitted normal distribution.
#
# Conclusion to look for:
# If actual 3-sigma days are much higher than expected normal-model 3-sigma days,
# the market has fat tails. Extreme events happen more often than the naive
# bell curve suggests.

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from scipy.stats import kurtosis, norm, probplot
from tabulate import tabulate

try:
    from IPython.display import display, HTML
except ImportError:
    display = None


TICKERS = {
    "HSI": "^HSI",
    "S&P 500": "^GSPC",
}

PERIOD = "5y"
SIGMA_THRESHOLD = 3
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


data = yf.download(
    list(TICKERS.values()),
    period=PERIOD,
    auto_adjust=True,
    progress=False
)

prices = data["Close"]

reverse_names = {
    "^HSI": "HSI",
    "^GSPC": "S&P 500",
}

prices = prices.rename(columns=reverse_names)

# Handle pandas version compatibility for pct_change
# pandas < 2.0 uses fill_method parameter
# pandas >= 2.0 deprecated fill_method
try:
    returns = prices.pct_change(fill_method=None).dropna()
except TypeError:
    # pandas >= 2.0
    returns = prices.pct_change().dropna()

results = []

for asset in returns.columns:
    r = returns[asset].dropna()

    mean = r.mean()
    std = r.std()

    raw_kurtosis = kurtosis(r, fisher=False)
    excess_kurtosis = kurtosis(r, fisher=True)

    upper_3sigma = mean + SIGMA_THRESHOLD * std
    lower_3sigma = mean - SIGMA_THRESHOLD * std

    extreme_days = (r > upper_3sigma) | (r < lower_3sigma)

    actual_3sigma_days = extreme_days.sum()
    actual_3sigma_frequency = extreme_days.mean()

    # A standard normal distribution has equal left and right tails.
    # 1 - norm.cdf(3) is the probability of being above +3 sigma.
    # Multiplying by 2 counts both tails: below -3 sigma and above +3 sigma.
    normal_3sigma_frequency = 2 * (1 - norm.cdf(SIGMA_THRESHOLD))

    expected_3sigma_days = normal_3sigma_frequency * len(r)

    danger_ratio = actual_3sigma_days / expected_3sigma_days

    results.append({
        "Asset": asset,
        "Kurtosis": raw_kurtosis,
        "Excess Kurtosis": excess_kurtosis,
        "Actual 3-sigma days": actual_3sigma_days,
        "Expected 3-sigma days under normal": expected_3sigma_days,
        "Actual 3-sigma frequency": actual_3sigma_frequency,
        "Normal 3-sigma frequency": normal_3sigma_frequency,
        "Danger ratio": danger_ratio,
    })

results_df = pd.DataFrame(results)

# Create clean display table
display_data = []
for _, row in results_df.iterrows():
    display_data.append([
        row["Asset"],
        f"{row['Kurtosis']:.2f}",
        f"{row['Excess Kurtosis']:.2f}",
        f"{row['Actual 3-sigma days']:.0f}",
        f"{row['Expected 3-sigma days under normal']:.1f}",
        f"{row['Actual 3-sigma frequency']:.2%}",
        f"{row['Normal 3-sigma frequency']:.2%}",
        f"{row['Danger ratio']:.1f}x",
    ])

headers = [
    "Asset",
    "Kurtosis",
    "Excess Kurt",
    "Actual 3σ Days",
    "Expected 3σ Days",
    "Actual Freq",
    "Normal Freq",
    "Danger Ratio"
]

print("\n" + "="*100)
print("FAT TAIL DETECTOR: Do Markets Have Fatter Tails Than Normal Distribution Predicts?")
print("="*100 + "\n")

print(tabulate(display_data, headers=headers, tablefmt="grid"))

print("\n" + "="*100)
print("INTERPRETATION")
print("="*100 + "\n")

for _, row in results_df.iterrows():
    asset = row["Asset"]
    expected = row["Expected 3-sigma days under normal"]
    actual = row["Actual 3-sigma days"]
    danger = row["Danger ratio"]
    
    print(f"{asset}:")
    print(f"  • Normal model predicted:  {expected:.1f} extreme days over 5 years")
    print(f"  • Actually observed:       {actual:.0f} extreme days")
    print(f"  • Reality vs. Normal:      {danger:.1f}x MORE dangerous than expected")
    print()

print("="*100)
print("CONCLUSION")
print("="*100)
print("""
Markets exhibit FAT TAILS. Extreme moves happen much more frequently than
a normal distribution would predict. This means:

✓ Risk models assuming normal distribution significantly underestimate crash risk
✓ Leverage and oversized positions are riskier than naive statistics suggest
✓ Quant strategies must account for tail events and correlation breakdowns
""")
print("="*100 + "\n")

# Generate visualization
OUTPUT_DIR.mkdir(exist_ok=True)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for ax, asset in zip(axes, returns.columns):
    r = returns[asset].dropna()
    probplot(r, dist="norm", plot=ax)
    ax.set_title(f"{asset}: QQ-Plot vs Normal Distribution", fontsize=12, fontweight="bold")
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "qq_plots_vs_normal.png", dpi=150, bbox_inches="tight")
print(f"✓ Chart saved to: {OUTPUT_DIR / 'qq_plots_vs_normal.png'}")
plt.show()

# Final interpretation:
# A straight QQ-plot line would suggest normally distributed returns.
# When the tail points bend away from the line, the market has more extreme
# observations than the normal model expects.

# Macro quant takeaway:
# Do not rely blindly on normal-distribution risk models. They often underestimate
# crash risk, which can lead to oversized positions and excessive leverage.
