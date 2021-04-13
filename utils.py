import pandas as pd


def get_weekdays_between(start, end):
    return pd.date_range(start=pd.to_datetime(start, format="%Y-%m-%d"),
                         end=pd.to_datetime(end, format="%Y-%m-%d")
                         ).to_series(
                         ).map(lambda x:
                               1 if is_weekday(x) else 0).sum()


def get_first_weekday_before(datetime):
    next_dt = datetime - pd.Timedelta('1 days')
    if is_weekday(next_dt):
        return next_dt
    else:
        return get_first_weekday_before(next_dt)


def is_weekday(datetime):
    return datetime.isoweekday() in range(1, 6)
