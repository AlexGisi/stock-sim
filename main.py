import pandas as pd
import numpy as np
import quandl
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
QUANDL_AUTH = "fdcJB3tASsz6tujQXJoQ"

msft = quandl.get("EOD/MSFT",
                  authtoken="fdcJB3tASsz6tujQXJoQ",
                  start_date='2015-12-28',
                  end_date='2017-12-28'
                  ).reset_index(drop=False)[['Date', 'Close']]


plt.figure(figsize=(15, 5))
plt.plot(msft['Date'], msft['Close'])
plt.xlabel('Days')
plt.ylabel('MSFT Price')
plt.show()
