import pandas as pd

from entity.stock_data import RawData
from entity.user_data import Portfolio


def percent_change(ticker, df):
    """
    Returns a percent change column for <ticker> from its YFinance <df>

    Percent change is calculated as follows:
     - percentage change in opening prices
       - [Open(n) - Open(n-1)] / Open(n-1)
     - add percentage change gained from previous period due to dividends
       - Dividends(n-1) / Open(n-1)
    :param ticker:
    :param df:
    :return:
    """
    pc = (df[f'{ticker}_Open'].diff() / df[f'{ticker}_Open'].shift(1))
    pc += (df[f'{ticker}_Dividends'] / df[f'{ticker}_Open']).shift(1)
    return pc


def get_portfolio_df(portfolio: Portfolio, data_store: RawData):
    """
    Gets portfolio df with percent change per period.

    Dataframe that is returned may have NaN values

    Assumption: all tickers in portfolio are in the data store
    :param portfolio:
    :param data_store:
    :return:
    """
    stock_dict = dict()
    fixed_rate = []
    for ticker in portfolio.symbols:
        if ticker in data_store.fixed_rate_assets:
            fixed_rate.append(ticker)
        else:
            stock_dict[ticker] = percent_change(ticker, data_store[ticker])

    ret_df = pd.DataFrame(stock_dict)
    for f in fixed_rate:
        # TODO assumes monthly compounding on all assets for now so...
        ret_df[f] = data_store.fixed_rate_assets[f]['rate'] / 12

    return ret_df[portfolio.symbols]


def filter_df(df, start_date=None, end_date=None):
    """
    Filters <df> to be between [start_date, end_date].

    Dates must be datetime objects.
    :param df: unfiltered df, index must be dates
    :param start_date:
    :param end_date:
    :return: filtered df
    """
    if start_date is not None:
        df = df[df.index >= start_date]
    if end_date is not None:
        df = df[df.index <= end_date]
    return df


def get_cov_expected(df):
    """
    Returns the covariance matrix and expected values of the items in the df
    :param df: DataFrame
    :return: Covariance matrix and expected values
    """
    cov = df.cov()
    expected = df.mean()
    return cov, expected
