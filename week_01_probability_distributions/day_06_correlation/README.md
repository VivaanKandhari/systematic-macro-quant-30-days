# Day 6: Correlation - The Most Important Stat in Macro

## Concept

Correlation measures how two return series move together. A correlation near `+1` means they usually move in the same direction, near `-1` means they usually move in opposite directions, and near `0` means there is little linear relationship.

## Market Connection

Macro investors use correlation to understand diversification, risk concentration, and crisis behavior. A portfolio that looks diversified in calm markets can become much less diversified when correlations rise during stress.

## Mini-Project

`day_06_macro_correlation_dashboard.py` builds a macro correlation dashboard for:

- HSI
- S&P 500
- US 10Y Yield
- Gold
- USD/CNH
- Oil

The script prints clean tables for data coverage and the correlation matrix, saves a heatmap, and plots the rolling 60-day correlation between HSI and the S&P 500.

## Run

```bash
python week_01_probability_distributions/day_06_correlation/day_06_macro_correlation_dashboard.py
```

```bash
python week_01_probability_distributions/day_06_correlation/day_06_rolling_correlation.py
```

## Interpretation

Use the dashboard to answer:

- Which macro assets move together?
- Which assets diversify HSI exposure?
- Did HSI and S&P 500 correlation change during the COVID crash?
- Do correlations become more dangerous during stress periods?
