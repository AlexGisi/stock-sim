# Using data from start to before 2017-10-1, simulate until 2017-12-28.
# Reference:
# https://towardsdatascience.com/simulating-stock-prices-in-python-using-geometric-brownian-motion-8dfd6e8c6b18

import pandas as pd
import numpy as np
from Stock import Stock

START_DATE = '2015-12-28'
END_DATE = '2017-12-28'
PRED_START_DATE = '2017-10-1'
PRED_END_DATE = '2017-12-28'
SCENARIOS = 10

msft = Stock('MSFT')
msft.get(START_DATE, END_DATE)


def get_weekdays_between(start, end):
    return pd.date_range(start=pd.to_datetime(start,
                         format="%Y-%m-%d") + pd.Timedelta('1 days'),
                         end=pd.to_datetime(end,
                         format="%Y-%m-%d")).to_series(
                         ).map(lambda x:
                               1 if x.isoweekday() in range(1, 6) else 0).sum()


# msft.plot_full()


s0 = msft.closes[0]
dt = 1
T = get_weekdays_between(PRED_START_DATE, PRED_END_DATE)
N = T / dt
t = np.arange(1, int(N) + 1)
mu = np.mean(msft.returns)
sigma = np.std(msft.returns)
dW_scenarios = {str(scenario_num): np.random.normal(0, 1, int(N)) for scenario_num in range(1, SCENARIOS + 1)}
W_scenarios = {str(scenario_num): dW_scenarios[str(scenario_num)].cumsum() for scenario_num in range(1, SCENARIOS + 1)}

print(mu)
print(sigma)
print(dW_scenarios['1'])
print(W_scenarios['1'])
