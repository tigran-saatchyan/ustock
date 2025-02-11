from services.yfinance_client import YFinanceClient

def get_ticker_info(ticker_symbol):
    client = YFinanceClient()
    info = client.get_ticker_info(ticker_symbol)
    return {'ticker': ticker_symbol, 'data': info}

def get_ticker_history(ticker_symbol, start, end, interval):
    client = YFinanceClient()
    history = client.get_history(ticker_symbol, start, end, interval)
    return history

def get_ticker_dividends(ticker_symbol):
    client = YFinanceClient()
    dividends = client.get_dividends(ticker_symbol)
    return dividends

def get_ticker_splits(ticker_symbol):
    client = YFinanceClient()
    splits = client.get_splits(ticker_symbol)
    return splits

def get_ticker_recommendations(ticker_symbol):
    client = YFinanceClient()
    recs = client.get_recommendations(ticker_symbol)
    return recs

def get_ticker_calendar(ticker_symbol):
    client = YFinanceClient()
    calendar = client.get_calendar(ticker_symbol)
    return calendar

def get_ticker_sustainability(ticker_symbol):
    client = YFinanceClient()
    sustainability = client.get_sustainability(ticker_symbol)
    return sustainability

def get_ticker_holders(ticker_symbol):
    client = YFinanceClient()
    holders = client.get_holders(ticker_symbol)
    return holders

def get_ticker_news(ticker_symbol):
    client = YFinanceClient()
    news = client.get_news(ticker_symbol)
    return news
