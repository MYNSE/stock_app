from flask import Flask, send_from_directory, request, make_response

from entity.stock_data import RawData
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


if __name__ == '__main__':
    Flask.run(app)
