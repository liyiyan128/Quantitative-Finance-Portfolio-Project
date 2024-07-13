import backtrader as bt
import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm

'''
We need to have two class, one is just to identify if two stocks are correlated enough.
Then we will call the PairTrading class on the found two stocks.
'''


class PairTrading(bt.Strategy):
    """
    Pair trading strategy.
    """

    params = dict(
        # Used to calculate the z-score
        period=15, 
        # Used to calculate the indicator 
        ind_period=30,

        
        # Portfolio value is the total amount we possess, including cash and all the shares we are holding
        portfolio_value=10000,

        # The cash we can use to purchase shares
        # cash_value=10000,
        stake=10,


        # Position of stocks we are tracking.
        amount_0=0,
        amount_1=0,

        # This is the boundary we set for open the trade and close the trade, the open bounds are set to high z-score for both positive and negative range, as a large z-score signifies
        # the correlation faltered. If the z-score falls within the close range, it means both stocks are entering the correlation once again, this is when we close the trade.
        # They don't have to be symmetrical.
        open_upper=2,
        open_lower=2,
        close_upper=1,
        close_lower=-1,

        # Portion of portfolio_value we want to split into long and short trades
        long_portion=0.5,
        short_portion=0.5,

        # For this naive implementation, we will allow one trade to be open as it will be easier to allocate our fund, we can consider more rigorous fund allocating strategy in the future.
        opened_trade=False,
        # status=0,
        # stop_loss=3.0
    )

    def __init__(self):
        self.portfolio_value = self.params.portfolio_value
        # self.cash = self.params.cash
        self.amount_0 = self.params.amount_0
        self.amount_1 = self.params.amount_1
        self.upper_bound_open = self.params.open_upper
        self.lower_bound_open = self.params.open_lower
        self.upper_bound_close = self.params.close_upper
        self.lower_bound_close = self.params.close_lower
        self.long_portion = self.params.long_portion
        self.short_portion = self.params.short_portion
        self.opened_trade = self.params.opened_trade
        self.current_order = None

        self.ols = bt.indicators.OLS_TransformationN(self.data0, self.data1,
                                                    period=self.params.period,
                                                    plot=True
                                                    )
        self.zscore = self.ols.zscore


    def next(self):
        # This method should contain the logic of buy, sell, open, close and cancel.

        ## We only allow one trade as we mobolize all the fund
        # print(self.opened_trade)

        hedge_ratio = 6.424801269143515

        ## Opening a trade
        if not self.opened_trade and (self.zscore >= self.upper_bound_open or self.zscore <= self.lower_bound_open):
            self.opened_trade = True
            outperforming_stock = self.data0 if self.zscore > 0 else self.data1
            underperforming_stock = self.data0 if self.zscore < 0 else self.data1

            # In pair trading, we want to long the underperforming, short the outperforming. As we will gain profits when these stocks move back into the correlating state.
            # Outperforming stock would likely to suffer a drop, while underperforming stock might see an increase.


            # TODO: Investigate how to properly calculate order size
            if self.zscore > 0:
                long_fund = (hedge_ratio / (1 + hedge_ratio)) * self.portfolio_value
                short_fund = (1 / (1 + hedge_ratio)) * self.portfolio_value
            else:
                short_fund = (hedge_ratio / (1 + hedge_ratio)) * self.portfolio_value
                long_fund = (1 / (1 + hedge_ratio)) * self.portfolio_value

            long_size = long_fund / underperforming_stock.close[0]
            short_size = short_fund / outperforming_stock.close[0]

            self.buy(underperforming_stock, size=long_size)
            self.sell(outperforming_stock, size=short_size)



        elif self.opened_trade and (self.zscore <= self.upper_bound_close or self.zscore >= self.lower_bound_close):
            self.close(self.data0)
            self.close(self.data1)
            self.opened_trade = False

        

    # def stop(self):
    #     pass


if __name__ == '__main__':
    # create a "Cerebro" engine instance
    cerebro = bt.Cerebro()  

    # Create a data feed
    data0 = bt.feeds.PandasData(dataname=yf.download("GLD",
                                                    start="2023-07-13",
                                                    end="2024-07-12"))
    
    data1 = bt.feeds.PandasData(dataname=yf.download("GDX",
                                                    start="2023-07-13",
                                                    end="2024-07-12"))

    cerebro.adddata(data0, name='GLD')  # Add the data feed
    cerebro.adddata(data1, name='GDX')  # Add the data feed

    cerebro.addstrategy(PairTrading)  # Add the trading strategy
    cerebro.run()  # run it all
    cerebro.plot()  # and plot it with a single 
