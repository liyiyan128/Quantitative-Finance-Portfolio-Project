import backtrader as bt
import yfinance as yf


class PairTrading(bt.Strategy):
    """
    Pair trading strategy.
    """

    params = dict(
        period=15,
        portfolio_value=10000,
    )

    def __init__(self):
        self.potfolio_value = self.params.portfolio_value

        self.ols = bt.indicators.OLS_Transformation(data0, data1,
                                                    period=self.params.period,
                                                    plot=True
                                                    )
        self.zscore = self.ols.zscore
        ## check zscore with statsmodels.api.OLS

    def next(self):
        pass

    def stop(self):
        pass


if __name__ == '__main__':
    pass