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

pred_start_dt = get_first_weekday_before(pd.to_datetime(PRED_START_DATE, format="%Y-%m-%d"))
pred_end_dt = get_first_weekday_before(pd.to_datetime(PRED_END_DATE, format="%Y-%m-%d"))

msft = Stock('MSFT')
msft.get(START_DATE, END_DATE)


def get_pred_differences(stock, pred):
    d = pd.Series(index=pred.index)
    for day in pred.index:
        print(day, stock.closes[day], pred[day])
        d[day] = stock.closes[day] - pred[day]
    return d


def diff_get_mean():
    plt.figure(figsize=(20, 10))

    scen_diffs = pd.DataFrame()
    for i in range(SCENARIOS):
        pred = msft.prediction(pred_start_dt, pred_end_dt)
        scen_diff = get_pred_differences(msft, pred)
        plt.plot(scen_diff)
        scen_diffs = scen_diffs.append(pd.Series(scen_diff, name=i))

    sum = scen_diffs.sum(axis=0)
    mean = sum / scen_diffs.count(axis=0)
    plt.show()

    return mean


def plot(scens):
    plt.figure(figsize=(20, 10))
    for i in range(scens):
        plt.plot(msft.prediction(pred_start_dt, pred_end_dt))
    plt.show()


print(diff_get_mean())
