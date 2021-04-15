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
SCENARIOS = 10000

pred_start_dt = get_first_weekday_before(pd.to_datetime(PRED_START_DATE, format="%Y-%m-%d"))
pred_end_dt = get_first_weekday_before(pd.to_datetime(PRED_END_DATE, format="%Y-%m-%d"))

msft = Stock('MSFT')
msft.get(START_DATE, END_DATE)


def get_pred_difference(stock, pred, pred_dates):
    pred_start_index = get_index(stock.dates, pred_dates[0])
    diffs = []

    print(len(stock.closes[pred_start_index:]))
    print(len(pred))

    print(stock.closes[pred_start_index:])
    print(pred)

    print(stock.dates[pred_start_index:].tolist())
    print(pred_dates)
    for i in range(1, len(pred)-2):
        diffs.append(stock.closes[i+pred_start_index] - pred[i])

    return diffs


def diff_sum():
    differences = pd.DataFrame()
    for i in range(SCENARIOS):
        pred = msft.prediction(pred_start_dt, pred_end_dt)
        # diffs = get_pred_difference(msft, pred, pred_dates)
        # differences = differences.append(pd.Series(data=diffs, name=i))


def plot(scens):
    plt.figure(figsize=(20, 10))
    for i in range(scens):
        plt.plot(msft.prediction(pred_start_dt, pred_end_dt))
    plt.show()


plot(SCENARIOS)

