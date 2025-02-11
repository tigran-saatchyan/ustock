"""
This module provides service functions to retrieve various types of data
from the yFinance API using the YFinanceClient.

Each function instantiates a YFinanceClient and calls the corresponding
method to obtain the data, then returns the result (or wraps it in a dictionary).
"""

from services.yfinance_client import YFinanceClient


def get_ticker_info(ticker_symbol):
    """Retrieve general information for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which information is requested.

    Returns:
        dict: A dictionary with two keys:
            - 'ticker': The provided ticker symbol.
            - 'data': A dictionary containing the ticker information obtained from YFinanceClient.
    """
    client = YFinanceClient()
    info = client.get_ticker_info(ticker_symbol)
    return {'ticker': ticker_symbol, 'data': info}


def get_ticker_history(ticker_symbol, start, end, interval):
    """Retrieve historical price data for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol.
        start (str): The start date for the historical data in 'YYYY-MM-DD' format.
        end (str): The end date for the historical data in 'YYYY-MM-DD' format.
        interval (str): The data interval (e.g. '1d', '1wk', '1mo').

    Returns:
        dict or list: The historical data as returned by the YFinanceClient. The exact format depends on the API response.
    """
    client = YFinanceClient()
    history = client.get_history(ticker_symbol, start, end, interval)
    return history


def get_ticker_dividends(ticker_symbol):
    """Retrieve dividend data for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which dividend data is requested.

    Returns:
        dict: A dictionary containing dividend data for the specified ticker.
    """
    client = YFinanceClient()
    dividends = client.get_dividends(ticker_symbol)
    return dividends


def get_ticker_splits(ticker_symbol):
    """Retrieve stock split data for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which split data is requested.

    Returns:
        dict: A dictionary containing stock split data for the specified ticker.
    """
    client = YFinanceClient()
    splits = client.get_splits(ticker_symbol)
    return splits


def get_ticker_recommendations(ticker_symbol):
    """Retrieve analyst recommendations for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which recommendations are requested.

    Returns:
        dict: A dictionary containing analyst recommendations for the specified ticker.
    """
    client = YFinanceClient()
    recs = client.get_recommendations(ticker_symbol)
    return recs


def get_ticker_calendar(ticker_symbol):
    """Retrieve the event calendar data for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which event calendar data is requested.

    Returns:
        dict: A dictionary containing event calendar information (such as earnings dates, announcements, etc.) for the specified ticker.
    """
    client = YFinanceClient()
    calendar = client.get_calendar(ticker_symbol)
    return calendar


def get_ticker_sustainability(ticker_symbol):
    """Retrieve ESG/sustainability data for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which sustainability data is requested.

    Returns:
        dict: A dictionary containing sustainability (ESG) metrics for the specified ticker.
    """
    client = YFinanceClient()
    sustainability = client.get_sustainability(ticker_symbol)
    return sustainability


def get_ticker_holders(ticker_symbol):
    """Retrieve holders data for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which holders information is requested.

    Returns:
        dict: A dictionary containing data about institutional and major holders for the specified ticker.
    """
    client = YFinanceClient()
    holders = client.get_holders(ticker_symbol)
    return holders


def get_ticker_news(ticker_symbol):
    """Retrieve news data for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which news is requested.

    Returns:
        dict: A dictionary containing news articles and related information for the specified ticker.
    """
    client = YFinanceClient()
    news = client.get_news(ticker_symbol)
    return news
