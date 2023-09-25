import stock_server as Server

import time


def test_add_remove():
    Server.add_stock_to_portfolio('O')
    time.sleep(1)
    Server.add_stock_to_portfolio('VGT')
    Server.add_fixed_rate({'symbol': 'CASH', 'rate': 0.04})
    Server.remove_symbol_from_portfolio('VGT')
    Server.add_stock_to_portfolio('VGT')
    assert Server.USER_DATA.current_portfolio.symbols == ['O', 'fixed_CASH', 'VGT']


if __name__ == '__main__':
    import pytest

    pytest.main(['server_test.py'])
