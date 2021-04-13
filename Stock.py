import quandl
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from quandl_auth import QUANDL_AUTH

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
