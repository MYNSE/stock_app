class Portfolio:
    def __init__(self):
        """
        Fixed rate assets is a dictionary of {symbol: monthly %change}
        Symbols is an ordered list of symbols representing the portfolio
        """
        self.fixed_rate_assets = dict()
        self.symbols = []


class UserData:
    """
    User Data object that stores their fixed rate assets, and portfolios
    """
    def __init__(self):
        self.fixed_rate_assets = dict()
        self.portfolios = dict()
        self.current_portfolio = None

    def get_portfolio(self, portfolio_name):
        """
        Gets a portfolio from the user's data. Creates a new portfolio if the name didn't exist.
        :param portfolio_name: The name of the portfolio to return
        :return: The portfolio
        """
        if portfolio_name not in self.portfolios:
            self.portfolios[portfolio_name] = Portfolio()
        self.current_portfolio = self.portfolios[portfolio_name]
        return self.current_portfolio
