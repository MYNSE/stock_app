from util import download_data as dd

import requests

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

    def add_ticker_data(self, ticker):
        """
        Adds ticker data to the data store.

        :param ticker:
        :return: Whether the operation was successful
        """
        if ticker in self.data:
            return True

        # Download the data
        try:
            ticker_data = dd.download_ticker_data(ticker, period='max', interval='1mo')
        except requests.exceptions.HTTPError:
            return False

        if len(ticker_data):
            self.data[ticker] = ticker_data
            return True
        return False

    def __contains__(self, ticker):
        """
        Checks if we have data for a specific ticker
        :param ticker: the ticker to look for
        :return: Whether the ticker is in our data storage
        """
        return ticker in self.data
