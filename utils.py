import pandas as pd


def get_weekdays_between(start_dt, end_dt):
    return pd.date_range(start=start_dt,
                         end=end_dt
                         ).to_series(
                         ).map(lambda x:
                               1 if is_weekday(x) else 0).sum()


def get_first_weekday_before_in(dt, index):
    next_dt = dt - pd.Timedelta('1 days')
    if is_weekday(next_dt) and next_dt in index:
        return next_dt
    else:
        return get_first_weekday_before_in(next_dt, index)


def is_weekday(dt):
    return dt.isoweekday() in range(1, 6)


def get_index(series, pd_datetime):
    try:
        return series.tolist().index(pd_datetime)
    except ValueError:
        return get_index(series, pd_datetime - pd.Timedelta("1 Days"))
