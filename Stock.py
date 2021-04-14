import quandl
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from quandl_auth import QUANDL_AUTH
import numpy as np
from utils import *

register_matplotlib_converters()


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data_start = None
        self.data_end = None
        self.dates = None
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
        self.dates = data['Date']
        self.closes = data['Close']

        self.returns = ((self.closes - self.closes.shift(1)) / self.closes.shift(1)).tolist()
        self.returns[0] = 0

    def plot_full(self):
        plt.figure(figsize=(15, 5))
        plt.plot(self.dates, self.closes)
        plt.xlabel('Days')
        plt.ylabel(self.ticker + ' Price')
        plt.show()

    def prediction(self, start_dt, end_dt):
        """
        Calculate a random path for the stock between start_dt, end_dt given parameters up to start_dt assuming GBM.
        Returns an Series of prices and the corresponding Series of Datetimes
        :param start_dt: pandas Datetime
        :param end_dt: pandas Datetime
        :return: Tuple, (Series, Series)
        """
        pred_start_index = get_index(self.dates, start_dt)

        s0 = self.closes[0]
        dt = 1
        T = get_weekdays_between(start_dt, end_dt)
        N = T / dt
        t = np.arange(1, int(N) + 1)
        mu = np.mean(self.returns[:pred_start_index])
        sigma = np.std(self.returns[:pred_start_index])
        dW = np.random.normal(0, 1, int(N))
        W = dW.cumsum()

        drift = (mu - 0.5 * sigma ** 2) * t
        diffusion = sigma * W

        pred = np.array(s0 * np.exp(drift + diffusion))
        pred = np.insert(pred, 0, s0)

        pred_date_range = pd.date_range(start=get_first_weekday_before(pd.to_datetime(start_dt, format="%Y-%m-%d")),
                                        end=pd.to_datetime(end_dt, format="%Y-%m-%d"),
                                        freq='D'
                                        ).map(lambda x:
                                              x if is_weekday(x) else np.nan).dropna()

        return pred, pred_date_range
