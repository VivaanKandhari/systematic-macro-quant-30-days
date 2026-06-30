# Day 5: Skewness & Asymmetric Returns

## Concept

Skewness measures whether return extremes are balanced or lopsided. Negative skew means the downside tail is larger than the upside tail; positive skew means the upside tail is larger.

## Market Connection

Macro investors care about skew because two assets can have similar average returns and volatility, but one can hide much worse crash risk.

## Mini-Project

`day_05_skewness_across_assets.py` compares skewness across:

- HSI
- Gold
- Long-term US Treasuries
- US Dollar
- Bitcoin

The script prints a clean ASCII table sorted from most negative skew to most positive skew, then saves side-by-side return histograms.

## Run

```bash
python week_01_probability_distributions/day_05_skewness/day_05_skewness_across_assets.py
```

## Interpretation

- `Skew < 0`: downside tail is worse.
- `Skew > 0`: upside tail is larger.
- `Worst Day` and `Best Day` show the actual observed extremes behind the statistic.

The key research question is:

> If I could only hold one asset during a crisis, which one looks least exposed to downside asymmetry?
