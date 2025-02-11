from services.yfinance_client import YFinanceClient

def get_options_dates(ticker_symbol):
    client = YFinanceClient()
    return client.get_options_dates(ticker_symbol)

def get_option_chain(ticker_symbol, date):
    client = YFinanceClient()
    return client.get_option_chain(ticker_symbol, date)
