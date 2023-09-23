import torch
from tqdm import tqdm


def make_gd_args(gd_params_dict):
    """
    Makes the arguments for GDPortfolio.gd_portfolio() from
    the gd parameters dict stored in user_data.gd_params
    :param gd_params_dict: gd_params dictionary
    :return: kwargs
    """
    args = {'epochs': 1000, 'lr': 1,
            'mult_exp': gd_params_dict['EXP']['gain'],
            'mult_var': gd_params_dict['VAR']['gain'],
            'mult_max_prop': gd_params_dict['MAX_PROP']['gain'],
            'max_prop_ub': gd_params_dict['MAX_PROP']['bound'],
            'indices_and_multiplier': gd_params_dict['INDIVIDUAL']}
    return args


class GDPortfolio:
    def __init__(self, df, cov, exp):
        """
        Initializes a GDPortfolio
        :param df: df of periodic gains of various assets
        :param cov: covariance matrix of the assets, in order
        :param exp: expected values of the assets, in order
        """
        self.df, self.cov, self.exp = df, cov, exp
        self.symbols = list(exp.index)
        self.cov_torch = torch.from_numpy(self.cov.to_numpy())
        self.exp_torch = torch.from_numpy(self.exp.to_numpy()).unsqueeze(1)

        self.start = torch.zeros_like(self.exp_torch)
        self.start.requires_grad = True

    def gd_portfolio(self, epochs=1000, lr=1, mult_exp=1, mult_var=1,
                     mult_max_prop=0, max_prop_ub=0.5,
                     indices_and_multiplier=None):
        """
        Runs gradient descent to optimize the portfolio.

        Add gain values for various losses

        :param epochs:
        :param lr:
        :param mult_exp: -exp of resulting portfolio
        :param mult_var: var of resulting portfolio
        :param mult_max_prop: max proportion gain
        :param max_prop_ub: max proportion in one single stock
        :param indices_and_multiplier: list of (multiplier, indices, max_bound, use_l2(vs upper bound only))
        :return: None
        """
        if indices_and_multiplier is None:
            indices_and_multiplier = []
        opt = torch.optim.SGD([self.start], lr=lr)
        for _ in tqdm(range(epochs)):
            opt.zero_grad()
            results = self._run_with_start(self.start)
            loss = (mult_exp * self._get_exp_loss(results) +
                    mult_var * self._get_var_loss(results) +
                    mult_max_prop * self._get_max_prop_loss(results, max_prop_ub))
            for m, indices, ub, l2 in indices_and_multiplier:
                loss += m * self._get_max_prop_loss_category(results, indices, ub, l2)

            loss.backward()
            opt.step()

    def get_proportions_list(self):
        """
        Get current stock proportions as a list
        """
        with torch.no_grad():
            proportions = torch.nn.functional.softmax(self.start, dim=0)
            return proportions.flatten().numpy().tolist()

    def get_exp_var(self, proportions=None):
        """
        Get expected value and variance of a portfolio
        :param proportions: Optional, manual list of proportions or dictionary
        :return:
        """
        with torch.no_grad():
            # convert dict to list if necessary
            if isinstance(proportions, dict):
                proportions = self.proportions_dict_to_list(proportions)

            if isinstance(proportions, list):
                proportions = torch.DoubleTensor(proportions).unsqueeze(1)
            else:
                proportions = torch.nn.functional.softmax(self.start, dim=0)
            results = self._run(proportions)
            var = results['cov_matrix'].sum().item()
            exp = results['expected_vals'].sum().item()
            return {'var': var, 'exp': exp}

    def proportions_dict_to_list(self, dic):
        """
        Converts dictionary of symbol: proportion to an ordered list
        corresponding to the symbols in the portfolio
        :param dic: the dictionary
        :return:
        """
        return [dic[s] if s in dic else 0. for s in self.symbols]

    def _run(self, proportions):
        # start will be n x 1
        prop_matrix = proportions @ proportions.transpose(0, 1)
        cov_matrix = self.cov_torch * prop_matrix

        expected_vals = proportions.transpose(0, 1) @ self.exp_torch

        return {'proportions': proportions,
                'cov_matrix': cov_matrix,
                'expected_vals': expected_vals}

    def _run_with_start(self, start):
        # runs _run after softmaxing <start>
        proportions = torch.nn.functional.softmax(start, dim=0)
        return self._run(proportions)

    # LOSSES ##################################################
    @staticmethod
    def _get_exp_loss(results_dict):
        return -results_dict['expected_vals'].sum()

    @staticmethod
    def _get_var_loss(results_dict):
        return results_dict['cov_matrix'].sum()

    @staticmethod
    def _get_max_prop_loss(results_dict, upper_bound):
        """
        Returns a positive value if maximum proportion of a single stock is
        above <upper_bound>, 0 otherwise
        :param results_dict: results from run()
        :param upper_bound: upper bound in [0, 1]
        :return:
        """
        max_prop = results_dict['proportions'].max()
        return torch.nn.functional.relu(max_prop - upper_bound)

    @staticmethod
    def _get_max_prop_loss_category(results_dict, indices, bound, l2=False):
        """
        Returns a positive value if maximum proportion of stocks at <indices>
        is greater than <upper_bound>, 0 otherwise.
        :param results_dict:
        :param indices:
        :param bound:
        :return:
        """
        r = results_dict['proportions'][indices, ...]
        prop = r.sum()
        if not l2:
            return torch.nn.functional.relu(prop - bound)
        else:
            return (prop - bound) ** 2
