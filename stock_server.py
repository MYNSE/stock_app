from entity.stock_data import RawData, get_fixed_symbol
from entity.user_data import UserData
from data_transfer.webapp_wrapper import user_data_to_json

import util.misc as MU
import gdportfolio.transform_data as TD
import gdportfolio.createportfolio as CP

# Generate basic user entities
DATA_STORE = RawData()
USER_DATA = UserData()
USER_DATA.get_portfolio('portfolio')  # TODO single portfolio for now, add more later


def add_stock_to_portfolio(ticker):
    """
    Adds a stock to the users' currently active portfolio
    :param ticker: The ticker to add
    """
    portfolio = USER_DATA.current_portfolio

    if ticker in portfolio.symbols:
        return {'code': 400,
                'data': 'Symbol already exists in the portfolio.'}

    if not DATA_STORE.add_ticker_data(ticker):
        return {'code': 404, 'data': 'Data Fetching failed. Make sure ticker is on Yahoo Finance.'}

    portfolio.symbols.append(ticker)
    return {'code': 200, 'data': 'Portfolio: ' + str(portfolio.symbols)}


def add_fixed_rate(form):
    """
    Adds a fixed rate asset to the users' currently active portfolio

    Required fields:
     - symbol: the symbol to represent the item

    Optional fields:
     - rate, period: rate/period of the asset, to describe appreciation rate
    """
    ticker = form['symbol']
    ticker = get_fixed_symbol(ticker)

    if 'rate' in form:
        # TODO remember rate is annual, we then divide down by period
        info = {'rate': form['rate'],
                'period': 'monthly'}  # TODO change later
    else:
        info = None

    portfolio = USER_DATA.current_portfolio

    if ticker in portfolio.symbols:
        return {'code': 400,
                'data': 'Symbol already exists in the portfolio.'}

    if not DATA_STORE.add_fixed_rate(ticker, info):
        return {'code': 400,
                'data': 'Failed to create symbol. Make sure its name is unique'}

    portfolio.symbols.append(ticker)
    return {'code': 200,
            'data': 'Portfolio: ' + str(portfolio.symbols)}


def remove_symbol_from_portfolio(symbol):
    """
    Removes a symbol from the current portfolio
    :param symbol: The symbol to remove
    """
    portfolio = USER_DATA.current_portfolio
    if symbol in portfolio:
        portfolio.remove(symbol)
        return {'code': 200,
                'data': 'Portfolio: ' + str(portfolio.symbols)}
    else:
        return {'code': 400,
                'data': 'Symbol not found in current portfolio'}


def set_all_allocations(request_data):
    """
    Sets proportion allocations
    """
    portfolio = USER_DATA.current_portfolio

    if set(request_data.keys()) != set(portfolio.symbols):
        return {'code': 400,
                'data': "Failed. Make sure you include an allocation for each portfolio symbol."}

    portfolio.percentage_allocations = request_data
    return {'code': 200,
            'json': portfolio.percentage_allocations}


def set_gd_params(request_data):
    """
    Sets GD params.
    Resulting parameters must retain the same key structure, and have the same variable
    types.

    Pass in a json with the same structure as the existing parameters in order to overwrite
    shared fields
    """
    params = USER_DATA.gd_params

    MU.overwrite_existing_values_in_struct(params.params, request_data,
                                           check_same_type=True)

    return {'code': 200,
            'json': params.params}


def run_gd():
    """
    Runs gradient descent using currently set GD Parameters

    :return: Json response, containing exp, var and proportions of the portfolio.
    """
    port_df = TD.get_portfolio_df(USER_DATA.current_portfolio, DATA_STORE)
    cov, expected = TD.get_cov_expected(port_df)
    gdp = CP.GDPortfolio(port_df, cov, expected)
    gdp.gd_portfolio(**CP.make_gd_args(USER_DATA.gd_params.params))
    results = gdp.get_exp_var()
    results['prop_list'] = gdp.get_proportions_list()

    return {'code': 200,
            'json': results}


def return_user_data():
    """
    Returns all user data as a JSON
    :return:
    """
    return {'code': 200,
            'json': user_data_to_json(USER_DATA)}
