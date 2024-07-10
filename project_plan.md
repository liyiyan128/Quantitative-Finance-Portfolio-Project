# Project Plan

**TODOS**

Project 1

1. Explore trading strategies:<br>
   basic understanding, existing implementation
2. Get stock data, implement & backtest:<br>
   determine data source (e.g. Yahoo Finance) and pick stocks/options
3. Benchmark/evaluate various strategies:<br>
   e.g. return volatility, risk
4. Detailed doc on the results --> start Project 2


**Resource**

--- Forums ---

- [QuantNet](https://quantnet.com/)
- [QuantStart](https://www.quantstart.com/)
- [Wilmott](https://forum.wilmott.com/)

--- Articles & Blogs ---

- [Algorithmic Trading Strategies: Types, Steps, Modelling Ideas and Implementation](https://blog.quantinsti.com/algorithmic-trading-strategies/)

- [Ernest Chan's blog](https://epchan.blogspot.com/): quantitative investment and trading ideas, research, and analysis

--- Tech Stack ---

- [BackTrader](https://www.backtrader.com/): backtesting framework
- [Zipline](https://www.zipline.io/): algorithmic trading simulator with paper and live trading capabilities; back testing

- Interactive Brokers: trading platform (paper trading)
- [QuantConnect](https://www.quantconnect.com): algorithmic trading platform

--- Data ---

- Yahoo Finance
- [Alpha Vantage API](https://www.alphavantage.co/documentation/#)

--- General finance ---

- [Finance Training Courses](https://www.streetofwalls.com/finance-training-courses/#hedge-fund-training)
    - [Building an Investment Thesis](https://www.streetofwalls.com/finance-training-courses/hedge-fund-training/building-an-investment-thesis/)


## Project 1: Trading Strategy Implementation & Backtest

Explore various trading strategies:

- Dual class arbitrage<br>
  Taking advantage of the price discrepency that exists between stocks that have dual listings. (e.g. GOOG & GOOGL)

- Bollinger band strategy<br>
  Bollinger bands are calculated by taking the 20-day simple moving average (SMA) of a stock price and then calculating the upper and lower bounds as the SMA +- two standard deviations of the actual stock price.

- Sector-based pairs trading algorithm<br>
  Two assets within the same sector/industry will likely have similar performances and therefore any observed significant deviations in the prices of these assets can be capitalized on in the form of buying the falling asset or shorting the rising asset.

- Machine learning based trading algorithm


## Project 2: Option Pricing Model

Potential pricing models:

- Monte Carlo<br>
  Numerous random walks for the price of an underlying asset are generated, whereby each has its own associated payoff. These payoffs are averaged and discounted to today, ultimately revealing the price of the option.

- Binomial pricing model

- Black Scholes

