from flask import Flask, send_from_directory, request, make_response, jsonify, render_template

import stock_server as Server

app = Flask(__name__, template_folder='public')
app.config['SECRET_KEY'] = 'mysecret'


def create_response(args):
    # IF json and data, put data inside json and return it
    if 'json' in args and 'data' in args:
        args['json']['_extraData'] = args['data']
        args.pop('data')

    if 'json' in args:
        response = jsonify(args['json'])
    else:
        response = make_response()

    if 'data' in args:
        response.data = args['data']
    response.status_code = args['code']
    return response


# https://stackoverflow.com/questions/15117416/capture-arbitrary-path-in-flask-route
@app.route('/<path:path>')
def get_resource(path):
    """
    Fetches a resource from the 'public' folder
    :param path: path
    :return:
    """
    return send_from_directory('public', path)


@app.route('/')
def get_home():
    """
    Gets homepage
    :return:
    """
    return send_from_directory('public', 'index.html')


@app.route('/v1/get_user_data', methods=['POST'])
def get_user_data():
    response_args = Server.return_user_data()
    return create_response(response_args)


@app.route('/v1/add_stock', methods=['POST'])
def add_stock_to_portfolio():
    """
    Adds a stock to the users' currently active portfolio
    """
    data = request.get_json()
    ticker = data['ticker']
    response_args = Server.add_stock_to_portfolio(ticker)
    return create_response(response_args)


@app.route('/v1/add_fixed_rate', methods=['POST'])
def add_fixed_rate():
    """
    Adds a fixed rate asset to the users' currently active portfolio
    """
    response_args = Server.add_fixed_rate(request.get_json())
    return create_response(response_args)


@app.route('/v1/remove_symbol', methods=['POST'])
def remove_symbol_from_portfolio():
    """
    Removes a stock to the users' currently active portfolio
    """
    ticker = request.get_json()['symbol']
    response_args = Server.remove_symbol_from_portfolio(ticker)
    return create_response(response_args)


@app.route('/v1/add_category', methods=['POST'])
def add_category_to_portfolio():
    """
    Adds a category to the portfolio
    """
    cat_data = request.get_json()
    response_args = Server.add_category(cat_data)
    return create_response(response_args)


@app.route('/v1/remove_symbol_from_category', methods=['POST'])
def remove_symbol_from_category():
    """
    Remove symbol from category
    """
    cat_data = request.get_json()
    response_args = Server.remove_symbol_from_category(cat_data['symbol'], cat_data['category'])
    return create_response(response_args)


@app.route('/v1/set_all_allocations', methods=['POST'])
def set_all_allocations():
    """
    Sets categories
    """
    response_args = Server.set_all_allocations(request.get_json())
    return create_response(response_args)


@app.route('/v1/set_gd_params', methods=['POST'])
def set_gd_params():
    """
    Sets GD params
    """
    response_args = Server.set_gd_params(request.get_json())
    return create_response(response_args)


@app.route('/v1/run_gd', methods=['POST'])
def run_gd():
    """
    Runs gradient descent using currently set GD Parameters

    :return: Json response, containing exp, var and proportions of the portfolio.
    """
    response_args = Server.run_gd()
    return create_response(response_args)


if __name__ == '__main__':
    Flask.run(app)
