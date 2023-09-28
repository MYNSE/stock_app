import requests

BASE_URL = "http://127.0.0.1:5000/"


def add_stock(ticker):
    if ticker is None:
        data = None
    else:
        data = {'ticker': ticker}
    response = requests.post(BASE_URL + 'v1/add_stock', json=data)
    print(response.content)
    return response


def add_fixed(symbol, data=None):
    if data is None:
        data = dict()
    data['symbol'] = symbol
    response = requests.post(BASE_URL + 'v1/add_fixed_rate', json=data)
    print(response.content)
    return response


def remove_stock(symbol):
    response = requests.post(BASE_URL + 'v1/remove_symbol', json={'symbol': symbol})
    print(response.content)
    return response


def add_category(title, color, symbols):
    response = requests.post(BASE_URL + 'v1/add_category', json={'title': title, 'color': color, 'symbols': symbols})
    print(response.content)
    return response


def remove_from_category(symbol, category):
    response = requests.post(BASE_URL + 'v1/remove_symbol_from_category', json={'symbol': symbol, 'category': category})
    print(response.content)
    return response


def set_params(params):
    response = requests.post(BASE_URL + 'v1/set_gd_params', json=params)
    print(response.content)
    return response


def set_categories(data):
    response = requests.post(BASE_URL + 'v1/set_all_allocations', json=data)
    print(response.content)
    return response


def run_gd():
    response = requests.post(BASE_URL + 'v1/run_gd')
    print(response.content)
    return response


def get_data():
    response = requests.post(BASE_URL + 'v1/get_user_data')
    print(response.content)
    return response
