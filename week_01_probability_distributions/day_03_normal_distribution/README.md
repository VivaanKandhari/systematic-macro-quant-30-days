# Day 3: Normal Distribution & Market Tail Risk

## Concept

A normal distribution is a bell-curve model defined by mean and standard deviation. It is useful as a baseline, but market returns often violate the normality assumption in the tails.

## Market Connection

Risk managers care about probabilities such as `P(return < -3%)`. A normal model can estimate those probabilities, but historical market data often shows extreme losses happening more often than the model predicts.

## Mini-Project

Build an HSI Risk Probability Calculator that compares normal-model probabilities against actual historical frequencies.

## Outputs

- Mean daily return
- Daily volatility
- Normal probability vs historical probability for large moves
- Histogram of HSI returns overlaid with fitted normal distribution

## Research Conclusion

The fitted normal distribution may describe ordinary days reasonably well, but it can underestimate downside tail risk in equity markets.

