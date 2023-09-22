import yfinance as yf


def download_ticker_data(ticker, period='max', interval='1mo'):
    """
    Downloads ticker data from YFinance

    Columns should include Open, High, Low, Close, Volume, Dividends, Stock Splits, Capital Gains
    Columns will be prepended with <ticker>_ e.g. Open --> AAPL_Open

    :param ticker: Ticker
    :param period: Period for the data e.g. 5y, 10y, max
    :param interval: e.g. 1mo, 3mo, 1y
    :return: Dataframe containing historical data
    """
    tmp = yf.Ticker(ticker)
    hist = tmp.history(period=period, interval=interval)
    hist.columns = [ticker + '_' + colname for colname in hist.columns]
    return hist
