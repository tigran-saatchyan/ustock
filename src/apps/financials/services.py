from services.yfinance_client import YFinanceClient

def get_financials(ticker_symbol):
    client = YFinanceClient()
    return client.get_financials(ticker_symbol)

def get_quarterly_financials(ticker_symbol):
    client = YFinanceClient()
    return client.get_quarterly_financials(ticker_symbol)

def get_balance_sheet(ticker_symbol):
    client = YFinanceClient()
    return client.get_balance_sheet(ticker_symbol)

def get_quarterly_balance_sheet(ticker_symbol):
    client = YFinanceClient()
    return client.get_quarterly_balance_sheet(ticker_symbol)

def get_cashflow(ticker_symbol):
    client = YFinanceClient()
    return client.get_cashflow(ticker_symbol)

def get_quarterly_cashflow(ticker_symbol):
    client = YFinanceClient()
    return client.get_quarterly_cashflow(ticker_symbol)

def get_earnings(ticker_symbol):
    client = YFinanceClient()
    return client.get_earnings(ticker_symbol)

def get_quarterly_earnings(ticker_symbol):
    client = YFinanceClient()
    return client.get_quarterly_earnings(ticker_symbol)
