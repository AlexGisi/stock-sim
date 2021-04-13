# Using data from start to before 2017-10-1, simulate until 2017-12-28.
# Reference:
# https://towardsdatascience.com/simulating-stock-prices-in-python-using-geometric-brownian-motion-8dfd6e8c6b18

import numpy as np
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

pred_start_index = get_index(msft.dates, pd.to_datetime(PRED_START_DATE, format="%Y-%m-%d"))
pred_end_index = get_index(msft.dates, pd.to_datetime(PRED_END_DATE, format="%Y-%m-%d"))


s0 = msft.closes[0]
dt = 1
T = get_weekdays_between(PRED_START_DATE, PRED_END_DATE)
N = T / dt
t = np.arange(1, int(N)+1)
mu = np.mean(msft.returns[:pred_start_index])
sigma = np.std(msft.returns[:pred_start_index])
dW_scenarios = {str(scenario_num): np.random.normal(0, 1, int(N)) for scenario_num in range(1, SCENARIOS + 1)}
W_scenarios = {str(scenario_num): dW_scenarios[str(scenario_num)].cumsum() for scenario_num in range(1, SCENARIOS + 1)}

drift = (mu - 0.6 * sigma**2) * t
diffusion_scenarios = {str(scenario_num): sigma*W_scenarios[str(scenario_num)] for scenario_num in range(1,
                                                                                                         SCENARIOS + 1)}

preds = np.array([s0 * np.exp(drift + diffusion_scenarios[str(i)]) for i in range(1, SCENARIOS + 1)])
preds = np.hstack((np.array([[s0] for scenario_num in range(SCENARIOS)]), preds))

plt.figure(figsize=(20, 10))
pred_date_range = pd.date_range(start=get_first_weekday_before(pd.to_datetime(PRED_START_DATE, format="%Y-%m-%d")),
                                end=pd.to_datetime(PRED_END_DATE, format="%Y-%m-%d"),
                                freq='D'
                                ).map(lambda x:
                                      x if is_weekday(x) else np.nan).dropna()


for i in range(SCENARIOS):
    plt.plot(pred_date_range, preds[i])

plt.show()
