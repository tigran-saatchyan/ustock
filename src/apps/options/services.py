import logging
from services.yfinance_client import YFinanceClient
from services.mock_data.options_data import get_mock_data

logger = logging.getLogger(__name__)

# Set to True to always use mock data (for testing purposes)
USE_MOCK_DATA = False


def get_options_dates(ticker_symbol):
    """Retrieve options expiration dates for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which to retrieve options dates.

    Returns:
        list: A list of available options expiration dates for the ticker.
    """
    if USE_MOCK_DATA:
        return get_mock_data('options_dates', ticker_symbol)
        
    client = YFinanceClient()
    dates = client.get_options_dates(ticker_symbol)
    
    # If dates is None or empty, use mock data as fallback
    if not dates:
        logger.info(f"No options dates from YFinance for {ticker_symbol}, using mock data")
        return get_mock_data('options_dates', ticker_symbol)
        
    return dates


def get_option_chain(ticker_symbol, date):
    """Retrieve the options chain for the given ticker and expiration date.

    Args:
        ticker_symbol (str): The ticker symbol for which to retrieve the options chain.
        date (str): The expiration date (in "YYYY-MM-DD" format) for which the options chain is requested.

    Returns:
        dict: A dictionary containing the options chain data, typically including 'calls' and 'puts'.
    """
    if USE_MOCK_DATA:
        return get_mock_data('option_chain', ticker_symbol, date=date)
        
    client = YFinanceClient()
    chain = client.get_option_chain(ticker_symbol, date)
    
    # If chain is None or empty, use mock data as fallback
    if not chain or ('calls' not in chain or 'puts' not in chain):
        logger.info(f"No option chain from YFinance for {ticker_symbol} on {date}, using mock data")
        return get_mock_data('option_chain', ticker_symbol, date=date)
        
    return chain
