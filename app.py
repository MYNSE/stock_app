from flask import Flask, send_from_directory, request, make_response

from entity.stock_data import RawData, get_fixed_symbol
from entity.user_data import UserData

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

# Generate basic user entities
DATA_STORE = RawData()
USER_DATA = UserData()
USER_DATA.get_portfolio('portfolio')  # TODO single portfolio for now, add more later


# https://stackoverflow.com/questions/15117416/capture-arbitrary-path-in-flask-route
@app.route('/<path:path>')
def get_resource(path):
    """
    Fetches a resource from the 'public' folder
    :param path: path
    :return:
    """
    return send_from_directory('public', path)


@app.route('/v1/add_stock', methods=['POST'])
def add_stock_to_portfolio():
    """
    Adds a stock to the users' currently active portfolio

    Required fields:
     - ticker: the stock ticker
    """
    response = make_response()
    ticker = request.form['ticker']

    portfolio = USER_DATA.current_portfolio

    if ticker in portfolio.symbols:
        response.status_code = 400
        response.data = 'Symbol already exists in the portfolio.'
        return response

    if not DATA_STORE.add_ticker_data(ticker):
        response.status_code = 404
        response.data = 'Data Fetching failed. Make sure ticker is on Yahoo Finance.'
        return response

    portfolio.symbols.append(ticker)
    response.status_code = 200
    response.data = 'Portfolio: ' + str(portfolio.symbols)
    return response


@app.route('/v1/add_fixed_rate', methods=['POST'])
def add_fixed_rate():
    """
    Adds a fixed rate asset to the users' currently active portfolio

    Required fields:
     - symbol: the symbol to represent the item

    Optional fields:
     - rate, period: rate/period of the asset, to describe appreciation rate
    """
    response = make_response()
    ticker = request.form['symbol']
    ticker = get_fixed_symbol(ticker)

    if 'rate' in request.form:
        # TODO remember rate is annual, we then divide down by period
        info = {'rate': request.form['rate'],
                'period': 'monthly'}  # TODO change later
    else:
        info = None

    portfolio = USER_DATA.current_portfolio

    if ticker in portfolio.symbols:
        response.status_code = 400
        response.data = 'Symbol already exists in the portfolio.'
        return response

    if not DATA_STORE.add_fixed_rate(ticker, info):
        response.status_code = 400
        response.data = 'Failed to create symbol. Make sure its name is unique'
        return response

    portfolio.symbols.append(ticker)
    response.status_code = 200
    response.data = 'Portfolio: ' + str(portfolio.symbols)
    return response


if __name__ == '__main__':
    Flask.run(app)
