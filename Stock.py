import quandl
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from quandl_auth import QUANDL_AUTH
import numpy as np
from utils import *
from random import choice

register_matplotlib_converters()


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data_start = None
        self.data_end = None
        self.closes = None
        self.returns = None

    def get(self, start, end):
        self.data_start = start
        self.data_end = end

        data = quandl.get("EOD/" + self.ticker,
                          authtoken=QUANDL_AUTH,
                          start_date=start,
                          end_date=end,
                          ).reset_index(drop=False)[['Date', 'Close']]

        self.closes = pd.Series(data['Close'].tolist(),
                                index=pd.DatetimeIndex(data['Date'].tolist()))

        self.returns = ((self.closes - self.closes.shift(1)) / self.closes.shift(1))
        self.returns[0] = 0

    def plot_full(self):
        plt.figure(figsize=(15, 5))
        plt.plot(self.closes)
        plt.title("Daily Close of " + self.ticker + " from " + self.data_start + " to " + self.data_end)
        plt.xlabel('Date')
        plt.ylabel(self.ticker + ' Price')
        plt.show()

    def prediction(self, start_dt, end_dt):
        """
        Calculate a random path for the stock between start_dt, end_dt given parameters up to start_dt assuming GBM.
        Returns a predicted path.
        :param start_dt: pandas Datetime, stock must be traded that day.
        :param end_dt: pandas Datetime, stock must be traded that day.
        :return: Series
        """
        if start_dt not in self.closes.index:
            raise ValueError('start_dt not in self.closes.index')
        elif end_dt not in self.closes.index:
            raise ValueError('end_dt not in self.closes.index')

        pred_index = self.closes[start_dt:end_dt].index

        s0 = self.closes[get_first_weekday_before(start_dt)]
        mu = np.mean(self.returns[:start_dt])
        sigma = np.std(self.returns[:start_dt])
        dW = pd.Series(np.random.normal(0, 1, len(pred_index)), index=pred_index)
        W = dW.cumsum()

        drift = pd.Series(mu - 0.5 * sigma**2, index=pred_index)
        diffusion = sigma * W

        pred = pd.Series(s0 * np.exp(drift + diffusion), index=pred_index)
        pred = pred.shift(1, fill_value=s0)

        return pred
