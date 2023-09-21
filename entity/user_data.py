class Portfolio:
    def __init__(self):
        """
        Fixed rate assets is a dictionary of {symbol: monthly %change}
        Symbols is an ordered list of symbols representing the portfolio
        """
        self.fixed_rate_assets = dict()
        self.symbols = []

    def add_ticker(self, ticker, data_store):
        """
        Adds a ticker to the portfolio. Ensures data was correctly downloaded.
        :param ticker: The ticker to be added
        :param data_store: The data store responsible for fetching the information
        :return: Whether the operation was successful
        """
        if ticker in data_store:
            self.symbols.append(ticker)
            return True
        else:
            if data_store.add_ticker_data(ticker):
                self.symbols.append(ticker)
                return True
            else:
                return False

class UserData:
    def __init__(self):
        self.fixed_rate_assets = dict()
        self.portfolios = []