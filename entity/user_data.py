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
        if portfolio_name not in self.portfolios:
            self.portfolios[portfolio_name] = Portfolio()
        self.current_portfolio = self.portfolios[portfolio_name]
        return self.current_portfolio
