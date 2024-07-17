# Quantitative Finance Portfolio Project

**Table of Contents**
- [Quantitative Finance Portfolio Project](#quantitative-finance-portfolio-project)
  - [Trading Strategy Implementation \& Backtest](#trading-strategy-implementation--backtest)
    - [Pair Trading](#pair-trading)

## Trading Strategy Implementation & Backtest

### Pair Trading

Pair trading is a market-neutral investment strategy that aims to profit from price discrepancies between two historically correlated assets. The process begins with selecting a pair of assets, such as stocks from the same sector, that have shown a strong historical correlation. Statistical analysis, including methods like cointegration and z-score calculations, is used to establish a mean and standard deviation of their price ratio. Traders monitor this ratio and identify trading opportunities when the ratio deviates significantly from the mean, indicating that one asset is relatively undervalued and the other overvalued.

Upon detecting such divergences, traders take long positions on the undervalued asset and short positions on the overvalued asset, betting on the eventual reversion to the historical mean. This market-neutral stance mitigates exposure to broader market movements, reducing systemic risk. The strategy is effective in various market conditions and relies on rigorous statistical analysis and efficient execution. However, it also carries risks such as model risk, where the historical relationship may break down, and execution risk, where delays can affect profitability. Additionally, transaction costs need to be carefully managed to ensure the strategy remains profitable.

**Statistical Tests for Stationarity & Cointegration Assumptions**
