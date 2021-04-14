# Using data from start to before 2017-10-1, simulate until 2017-12-28.
# Reference:
# https://towardsdatascience.com/simulating-stock-prices-in-python-using-geometric-brownian-motion-8dfd6e8c6b18

from Stock import Stock
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import numpy as np
from utils import *

register_matplotlib_converters()

START_DATE = '2015-12-28'
END_DATE = '2017-12-28'
PRED_START_DATE = '2017-10-1'
PRED_END_DATE = '2017-12-28'
SCENARIOS = 1

pred_start_dt = pd.to_datetime(PRED_START_DATE, format="%Y-%m-%d")
pred_end_dt = pd.to_datetime(PRED_END_DATE, format="%Y-%m-%d")

msft = Stock('MSFT')
msft.get(START_DATE, END_DATE)


def get_pred_difference(stock, pred, pred_dates):
    pred_start_index = get_index(stock.dates, pred_dates[0])
    diffs = []

    for i in range(1, len(pred)-2):
        diffs.append(stock.closes[i+pred_start_index] - pred[i])

    return diffs


def plot(scenarios):
    plt.figure(figsize=(20, 10))
    for i in range(scenarios):
        pred, pred_date_range = msft.prediction(pred_start_dt,
                                                pred_end_dt)
        plt.plot(pred_date_range, pred)

    plt.show()


differences = []
for i in range(SCENARIOS):
    pred, pred_dates = msft.prediction(pred_start_dt, pred_end_dt)
    differences.append(get_pred_difference(msft, pred, pred_dates))

print(differences)

