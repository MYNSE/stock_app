class Portfolio:
    def __init__(self):
        """
        Fixed rate assets is a dictionary of {symbol: monthly %change}
        Symbols is an ordered list of symbols representing the portfolio
        """
        self.symbols = []
        self.percentage_allocations = dict()


class GDParams:
    """
    Storage class for Gradient Descent Parameters
    """
    def __init__(self):
        self.params = self.get_default_params()

    @staticmethod
    def get_default_params():
        """
        Gets default parameters to give to the user
        at the start of the program
        """
        sample_params = {
            'EXP': {'gain': 0},
            'VAR': {'gain': 0},
            'MAX_PROP': {'type': 'ReLU',
                         'bound': 0,
                         'gain': 0},
            'INDIVIDUAL': []
        }
        return sample_params

    def check_params_format(self, params, sample_params=None):
        """
        Checks that the params format is consistent with the format of <sample_params>.
        Key structure of <sample_params> must be a subset of the key structure of
        <params>, and the values corresponding to shared keys must be the same type.
        """
        # TODO currently unused
        if sample_params is None:
            sample_params = self.get_default_params()

        for k in sample_params:
            if k not in params:
                return False
            elif not isinstance(params[k], type(sample_params[k])):
                return False
            if isinstance(sample_params[k], dict):
                self.check_params_format(params[k], sample_params[k])
        return True


class UserData:
    """
    User Data object that stores their fixed rate assets, and portfolios
    """

    def __init__(self):
        self.portfolios = dict()
        self.current_portfolio = None
        self.gd_params = GDParams()

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
