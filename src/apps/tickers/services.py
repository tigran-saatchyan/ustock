"""
This module provides service functions to retrieve various types of data
from the yFinance API using the YFinanceClient.

Each function instantiates a YFinanceClient and calls the corresponding
method to obtain the data, then returns the result (or wraps it in a dictionary).

If the actual data from YFinance is empty or None, mock data is provided as a fallback.
"""

import logging
from services.yfinance_client import YFinanceClient
from services.mock_data.ticker_data import get_mock_data

logger = logging.getLogger(__name__)

# Set to True to always use mock data (for testing purposes)
USE_MOCK_DATA = False


def get_ticker_info(ticker_symbol):
    """Retrieve general information for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which information is requested.

    Returns:
        dict: A dictionary with two keys:
            - 'ticker': The provided ticker symbol.
            - 'data': A dictionary containing the ticker information obtained from YFinanceClient.
    """
    if USE_MOCK_DATA:
        return get_mock_data('info', ticker_symbol)
        
    client = YFinanceClient()
    info = client.get_ticker_info(ticker_symbol)
    
    # If info is None or empty, use mock data as fallback
    if not info:
        logger.info(f"No data from YFinance for {ticker_symbol}, using mock data")
        return get_mock_data('info', ticker_symbol)
        
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
    if USE_MOCK_DATA:
        return get_mock_data('history', ticker_symbol, start=start, end=end, interval=interval)['data']
        
    client = YFinanceClient()
    history = client.get_history(ticker_symbol, start, end, interval)
    
    # If history is None or empty, use mock data as fallback
    if not history:
        logger.info(f"No history data from YFinance for {ticker_symbol}, using mock data")
        return get_mock_data('history', ticker_symbol, start=start, end=end, interval=interval)['data']
        
    return history


def get_ticker_dividends(ticker_symbol):
    """Retrieve dividend data for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which dividend data is requested.

    Returns:
        dict: A dictionary containing dividend data for the specified ticker.
    """
    if USE_MOCK_DATA:
        return get_mock_data('dividends', ticker_symbol)['data']
        
    client = YFinanceClient()
    dividends = client.get_dividends(ticker_symbol)
    
    # If dividends is None or empty, use mock data as fallback
    if not dividends:
        logger.info(f"No dividend data from YFinance for {ticker_symbol}, using mock data")
        return get_mock_data('dividends', ticker_symbol)['data']
        
    return dividends


def get_ticker_splits(ticker_symbol):
    """Retrieve stock split data for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which split data is requested.

    Returns:
        dict: A dictionary containing stock split data for the specified ticker.
    """
    if USE_MOCK_DATA:
        return get_mock_data('splits', ticker_symbol)['data']
        
    client = YFinanceClient()
    splits = client.get_splits(ticker_symbol)
    
    # If splits is None or empty, use mock data as fallback
    if not splits:
        logger.info(f"No splits data from YFinance for {ticker_symbol}, using mock data")
        return get_mock_data('splits', ticker_symbol)['data']
        
    return splits


def get_ticker_recommendations(ticker_symbol):
    """Retrieve analyst recommendations for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which recommendations are requested.

    Returns:
        dict: A dictionary containing analyst recommendations for the specified ticker.
    """
    if USE_MOCK_DATA:
        return get_mock_data('recommendations', ticker_symbol)['data']
        
    client = YFinanceClient()
    recs = client.get_recommendations(ticker_symbol)
    
    # If recs is None or empty, use mock data as fallback
    if not recs:
        logger.info(f"No recommendations data from YFinance for {ticker_symbol}, using mock data")
        return get_mock_data('recommendations', ticker_symbol)['data']
        
    return recs


def get_ticker_calendar(ticker_symbol):
    """Retrieve the event calendar data for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which event calendar data is requested.

    Returns:
        dict: A dictionary containing event calendar information (such as earnings dates, announcements, etc.) for the specified ticker.
    """
    if USE_MOCK_DATA:
        return get_mock_data('calendar', ticker_symbol)['data']
        
    client = YFinanceClient()
    calendar = client.get_calendar(ticker_symbol)
    
    # If calendar is None or empty, use mock data as fallback
    if not calendar:
        logger.info(f"No calendar data from YFinance for {ticker_symbol}, using mock data")
        return get_mock_data('calendar', ticker_symbol)['data']
        
    return calendar


def get_ticker_sustainability(ticker_symbol):
    """Retrieve ESG/sustainability data for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which sustainability data is requested.

    Returns:
        dict: A dictionary containing sustainability (ESG) metrics for the specified ticker.
    """
    if USE_MOCK_DATA:
        return get_mock_data('sustainability', ticker_symbol)['data']
        
    client = YFinanceClient()
    sustainability = client.get_sustainability(ticker_symbol)
    
    # If sustainability is None or empty, use mock data as fallback
    if not sustainability:
        logger.info(f"No sustainability data from YFinance for {ticker_symbol}, using mock data")
        return get_mock_data('sustainability', ticker_symbol)['data']
        
    return sustainability


def get_ticker_holders(ticker_symbol):
    """Retrieve holders data for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which holders information is requested.

    Returns:
        dict: A dictionary containing data about institutional and major holders for the specified ticker.
    """
    if USE_MOCK_DATA:
        return get_mock_data('holders', ticker_symbol)['data']
        
    client = YFinanceClient()
    holders = client.get_holders(ticker_symbol)
    
    # If holders is None or empty, use mock data as fallback
    if not holders:
        logger.info(f"No holders data from YFinance for {ticker_symbol}, using mock data")
        return get_mock_data('holders', ticker_symbol)['data']
        
    return holders


def get_ticker_news(ticker_symbol):
    """Retrieve news data for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which news is requested.

    Returns:
        dict: A dictionary containing news articles and related information for the specified ticker.
    """
    if USE_MOCK_DATA:
        return get_mock_data('news', ticker_symbol)['data']
        
    client = YFinanceClient()
    news = client.get_news(ticker_symbol)
    
    # If news is None or empty, use mock data as fallback
    if not news:
        logger.info(f"No news data from YFinance for {ticker_symbol}, using mock data")
        return get_mock_data('news', ticker_symbol)['data']
        
    return news
