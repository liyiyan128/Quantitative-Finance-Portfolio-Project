import backtrader as bt
import yfinance as yf
import numpy as np
import pandas as pd
# import statsmodels.api as sm


class PairTrading(bt.Strategy):
    """
    Pair trading strategy.
    """

    params = dict(
        # Used to calculate the z-score
        period=10,

        # The entry and exit threshold for the z-score
        entry_threshold=1,
        exit_threshold=0.5,

        printlog=True,
    )

    def log(self, txt, dt=None):
        if self.params.printlog:
            dt = dt or self.data.datetime[0]
            dt = bt.num2date(dt)
            print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [bt.Order.Submitted, bt.Order.Accepted]:
            return  # await further notifications

        if order.status == order.Completed:
            if order.isbuy():
                buytxt = 'BUY COMPLETE, %.2f' % order.executed.price
                self.log(buytxt, order.executed.dt)
            else:
                selltxt = 'SELL COMPLETE, %.2f' % order.executed.price
                self.log(selltxt, order.executed.dt)

        elif order.status in [order.Expired, order.Canceled, order.Margin]:
            self.log('%s ,' % order.Status[order.status])
            pass  # simply log

        # Allow new orders
        self.orderid = None

    def __init__(self):
        self.orderid = None
        self.qty0 = 0  # number of shares for stock 0
        self.qty1 = 0  # number of shares for stock 1

        self.status = 0  # 0: no position, 1: long position, -1: short position

        self.ols = bt.indicators.OLS_TransformationN(self.datas[0], self.datas[1],
                                                     period=self.params.period,
                                                     plot=True
                                                     )
        self.zscore = self.ols.zscore

    def next(self):
        if self.orderid:
            return  # if an order is active, no new orders are allowed

        # Enter short position
        if self.status != -1 and self.zscore[0] > self.params.entry_threshold:
            cash = 0.5 * self.broker.get_cash()
            qty0 = int(cash / self.datas[0].close[0])  # number of shares for stock 0
            qty1 = int(cash / self.datas[1].close[0])  # number of shares for stock 1

            # place the order
            self.log('SELL CREATE %s, price = %.2f, qty = %d' % ("TICK0", self.datas[0].close[0], qty0+self.qty0))
            self.sell(data=self.datas[0], size=qty0+self.qty0)
            self.log('BUY CREATE %s, price = %.2f, qty = %d' % ("TICK1", self.datas[1].close[0], qty1+self.qty1))
            self.buy(data=self.datas[1], size=qty1+self.qty1)

            # update positions
            self.qty0 = qty0
            self.qty1 = qty1
            # update status
            self.status = -1  # short the spread

        # Enter long position
        elif self.status != 1 and self.zscore[0] < -self.params.entry_threshold:
            cash = 0.5 * self.broker.get_cash()
            qty0 = int(cash / self.datas[0].close[0])
            qty1 = int(cash / self.datas[1].close[0])

            # place the order
            self.log('BUY CREATE %s, price = %.2f, qty = %d' % ("TICK0", self.datas[0].close[0], qty0+self.qty0))
            self.buy(data=self.datas[0], size=qty0+self.qty0)
            self.log('SELL CREATE %s, price = %.2f, qty = %d' % ("TICK1", self.datas[1].close[0], qty1+self.qty1))
            self.sell(data=self.datas[1], size=qty1+self.qty1)

            # update positions
            self.qty0 = qty0
            self.qty1 = qty1
            # update status
            self.status = 1

        # Exit position
        elif abs(self.zscore) < self.params.exit_threshold:
            self.log('CLOSE %s, price = %.2f' % ("TICK0", self.datas[0].close[0]))
            self.close(self.datas[0])
            self.log('CLOSE %s, price = %.2f' % ("TICK1", self.datas[1].close[0]))
            self.close(self.datas[1])
            self.status = 0

            # update positions
            self.qty0 = 0
            self.qty1 = 0


if __name__ == '__main__':
    # create a "Cerebro" engine instance
    cerebro = bt.Cerebro()

    # Create a data feed
    data0 = bt.feeds.PandasData(dataname=yf.download("GLD",
                                                     start="2024-01-13",
                                                     end="2024-07-12"))

    data1 = bt.feeds.PandasData(dataname=yf.download("GDX",
                                                     start="2024-01-13",
                                                     end="2024-07-12"))

    cerebro.adddata(data0, name='GLD')  # Add the data feed
    cerebro.adddata(data1, name='GDX')  # Add the data feed

    cerebro.broker.setcash(10000)  # set cash
    cerebro.broker.setcommission(commission=0.001)  # set commission

    cerebro.addstrategy(PairTrading)  # Add the trading strategy

    cerebro.run()
    cerebro.plot()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
