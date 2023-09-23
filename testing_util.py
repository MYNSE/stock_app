import requests

BASE_URL = "http://127.0.0.1:5000/"


def add_stock(ticker):
    if ticker is None:
        data = None
    else:
        data = {'ticker': ticker}
    response = requests.post(BASE_URL + 'v1/add_stock', data=data)
    print(response.content)
    return response


def add_fixed(symbol, data=None):
    if data is None:
        data = dict()
    data['symbol'] = symbol
    response = requests.post(BASE_URL + 'v1/add_fixed_rate', data=data)
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
