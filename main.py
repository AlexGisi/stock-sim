# Using data from start to before 2017-10-1, simulate until 2017-12-28.
# Reference:
# https://towardsdatascience.com/simulating-stock-prices-in-python-using-geometric-brownian-motion-8dfd6e8c6b18

from Stock import Stock
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from utils import *

register_matplotlib_converters()

START_DATE = '2015-12-28'
END_DATE = '2017-12-28'
PRED_START_DATE = '2017-10-1'
PRED_END_DATE = '2017-12-28'
SCENARIOS = 1000

msft = Stock('MSFT')
msft.get(START_DATE, END_DATE)


plt.figure(figsize=(20, 10))


for i in range(SCENARIOS):
    pred, pred_date_range = msft.prediction(pd.to_datetime(PRED_START_DATE, format="%Y-%m-%d"),
                                            pd.to_datetime(PRED_END_DATE, format="%Y-%m-%d"))
    plt.plot(pred_date_range, pred)

plt.show()
