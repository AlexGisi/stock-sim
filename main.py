# Using data from start to before 2017-10-1, simulate until 2017-12-28.
# Reference:
# https://towardsdatascience.com/simulating-stock-prices-in-python-using-geometric-brownian-motion-8dfd6e8c6b18
# TODO: test 95% confidence. Does 95% of paths contain the true path 95% of the time?
# TODO: convergence of sim to exp.

from Stock import Stock
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from utils import *

register_matplotlib_converters()

START_DATE = '2015-12-28'
END_DATE = '2017-12-28'
PRED_START_DATE = '2017-10-1'
PRED_END_DATE = '2017-12-28'
SCENARIOS = 10

msft = Stock('AAPL')
msft.get(START_DATE, END_DATE)

pred_start_dt = get_first_weekday_before_in(pd.to_datetime(PRED_START_DATE, format="%Y-%m-%d"),
                                            msft.closes.index)
pred_end_dt = get_first_weekday_before_in(pd.to_datetime(PRED_END_DATE, format="%Y-%m-%d"),
                                          msft.closes.index)


def get_pred_differences(stock, pred):
    d = pd.Series(index=pred.index)
    for day in pred.index:
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
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111)

    means, drifts = msft.get_pred_mean(pred_start_dt, pred_end_dt)
    ax.plot(means, color="black", linestyle="dashed")
    final_mean = 0

    for i in range(scens):
        pred = msft.prediction(pred_start_dt, pred_end_dt)
        final_mean += pred[-1]
        ax.plot(pred)
    final_mean = final_mean / SCENARIOS

    plt.title(f"Predictions and expected mean (dashed) of MSFT stock from Oct. 1 to Dec. 28, 2017\n"
              f"Mean return: {drifts[1]:.6f}, terminal expected value: {means[-1]:.2f}, terminal average: "
              f"{final_mean:.2f}")
    plt.xlabel("Date")
    plt.ylabel("MSFT price")

    plt.show()


# diff_get_mean().to_csv(path_or_buf='res/diff.csv', header=False)

plot(SCENARIOS)
