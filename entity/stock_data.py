from util import download_data as dd

import requests


def get_fixed_symbol(ticker):
    """
    Gets the symbol for a fixed rate asset
    :param ticker: the symbol we are trying to fetch
    :return: a formatted symbol representing the fixed rate asset
    """
    return f"fixed_{ticker}" if 'fixed_' not in ticker else ticker


class RawData:
    """
    Raw Ticker Data.

    This data storage is responsible for downloading ticker data from Yahoo Finance
    For now, we will download 1-month data for the maximum period of time.
    This data storage will NOT store fixed-rate asset data.
    """

    def __init__(self):
        """
        Initializes an empty data store
        """
        # TODO in the future, this could scan the data folder and populate based on that.
        self.data = dict()
        self.fixed_rate_assets = dict()

    def add_ticker_data(self, ticker):
        """
        Adds ticker data to the data store.

        :param ticker:
        :return: Whether the operation was successful
        """
        if ticker in self.data:
            return True
        elif ticker in self.fixed_rate_assets:
            return False

        # Download the data
        try:
            ticker_data = dd.download_ticker_data(ticker, period='max', interval='1mo')
        except requests.exceptions.HTTPError:
            return False

        if len(ticker_data):
            self.data[ticker] = ticker_data
            return True
        return False

    def add_fixed_rate(self, ticker, info=None):
        """
        Adds a fixed rate asset to the data storage
        :param ticker: symbol to add
        :param info: Info about the asset. Must contain keys 'rate' and 'period'
        :return: whether the operation was successful
        """
        ticker = get_fixed_symbol(ticker)
        if ticker in self.fixed_rate_assets:
            return True
        elif ticker in self.data:
            return False

        # Prepare to add the new asset
        try:
            info['rate'] = float(info['rate'])
            assert 'period' in info
        except ValueError:
            return False
        except AssertionError:
            return False

        self.fixed_rate_assets[ticker] = info
        return True

    def __contains__(self, ticker):
        """
        Checks if we have data for a specific ticker
        :param ticker: the ticker to look for
        :return: Whether the ticker is in our data storage
        """
        return ticker in self.data
