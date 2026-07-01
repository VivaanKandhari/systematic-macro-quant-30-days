# Day 6: Correlation - The Most Important Stat in Macro

## Concept

Correlation measures how two return series move together. A correlation near `+1` means they usually move in the same direction, near `-1` means they usually move in opposite directions, and near `0` means there is little linear relationship.

The key macro lesson is that correlation is not fixed. Two assets can look weakly related over a full sample, but become much more connected during certain regimes.

## Market Connection

Macro investors use correlation to understand diversification, risk concentration, and crisis behavior.

A portfolio that looks diversified in calm markets can become much less diversified when correlations rise during stress. This is why macro researchers look at both:

- full-sample correlation
- rolling correlation through time

Full-sample correlation answers:

```text
How did these assets move together on average?
Rolling correlation answers:
Did the relationship change across regimes?
Projects
Day 6 now has two separate projects.
Project 1: Macro Correlation Dashboard
day_06_macro_correlation_dashboard.py builds a broad macro correlation dashboard for:
HSI
S&P 500
US 10Y Yield
Gold
USD/CNH
Oil
The script:
downloads real market data with yfinance
calculates daily returns
prints a clean data coverage table
prints the full correlation matrix
saves a correlation heatmap
Use this project to answer:
Which macro assets move together?
Which assets have weak relationships?
Which assets may diversify HSI exposure?
Does HSI behave more like a global equity asset or a local/China-driven market?
Project 2: Rolling Correlation Study
day_06_rolling_correlation.py focuses specifically on the rolling 60-day correlation between:
HSI
S&P 500
The script:
downloads HSI and S&P 500 data
converts prices into daily returns
calculates 60-day rolling correlation
plots how the relationship changes through time
marks important stress periods where relevant
Use this project to answer:
Is HSI/S&P 500 correlation stable?
When did the two markets become more synchronized?
Did correlation rise during stress periods?
When did local Hong Kong/China factors dominate global equity sentiment?
Run
Run the full macro correlation dashboard:
python week_01_probability_distributions/day_06_correlation/day_06_macro_correlation_dashboard.py
Run the separate rolling correlation project:
python week_01_probability_distributions/day_06_correlation/day_06_rolling_correlation.py
Interpretation
From the correlation matrix, focus on the size and sign of each relationship:
+0.70 to +1.00   strong positive relationship
+0.30 to +0.70   moderate positive relationship
-0.30 to +0.30   weak or little linear relationship
-0.70 to -0.30   moderate negative relationship
-1.00 to -0.70   strong negative relationship
From the rolling correlation chart, focus on whether the relationship changes over time.
A rising HSI/S&P 500 rolling correlation means:
Hong Kong equities and US equities are becoming more synchronized.
A falling or near-zero correlation means:
HSI is behaving more independently from US equities.
A negative rolling correlation means:
HSI and S&P 500 tended to move in opposite directions during that window.
Key Takeaway
Average correlation can hide regime changes.
A low full-sample HSI/S&P 500 correlation does not guarantee diversification. If rolling correlation rises during stress, the assets may become connected exactly when diversification is most needed.
The macro quant lesson:
Correlation is not a constant. It is a market regime variable
