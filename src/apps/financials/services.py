import logging
from services.yfinance_client import YFinanceClient
from services.mock_data.financials_data import get_mock_data

logger = logging.getLogger(__name__)

# Set to True to always use mock data (for testing purposes)
USE_MOCK_DATA = False


def get_financials(ticker_symbol):
    """Retrieve annual financial data for a given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which financial data is requested.

    Returns:
        dict: A dictionary containing the annual financial data for the specified ticker.
    """
    if USE_MOCK_DATA:
        data = get_mock_data('financials', ticker_symbol)
    else:
        client = YFinanceClient()
        data = client.get_financials(ticker_symbol)

        # If data is None or empty, use mock data as fallback
        if not data:
            logger.info(f"No financials data from YFinance for {ticker_symbol}, using mock data")
            data = get_mock_data('financials', ticker_symbol)

    # Transpose the data structure to match frontend expectations
    # Frontend expects: { 'Total Revenue': { '2023-12-31': 1000000, ... }, ... }
    # But we have: { '2023-12-31': { 'Total Revenue': 1000000, ... }, ... }
    transposed_data = {}

    for date, values in data.items():
        for item, value in values.items():
            if item not in transposed_data:
                transposed_data[item] = {}
            transposed_data[item][date] = value

    return transposed_data


def get_quarterly_financials(ticker_symbol):
    """Retrieve quarterly financial data for a given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which quarterly financial data is requested.

    Returns:
        dict: A dictionary containing the quarterly financial data for the specified ticker.
    """
    if USE_MOCK_DATA:
        data = get_mock_data('financials', ticker_symbol, quarterly=True)
    else:
        client = YFinanceClient()
        data = client.get_quarterly_financials(ticker_symbol)

        # If data is None or empty, use mock data as fallback
        if not data:
            logger.info(f"No quarterly financials data from YFinance for {ticker_symbol}, using mock data")
            data = get_mock_data('financials', ticker_symbol, quarterly=True)

    # Transpose the data structure to match frontend expectations
    transposed_data = {}

    for date, values in data.items():
        for item, value in values.items():
            if item not in transposed_data:
                transposed_data[item] = {}
            transposed_data[item][date] = value

    return transposed_data


def get_balance_sheet(ticker_symbol):
    """Retrieve annual balance sheet data for a given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which the balance sheet data is requested.

    Returns:
        dict: A dictionary containing the annual balance sheet data for the specified ticker.
    """
    if USE_MOCK_DATA:
        data = get_mock_data('balance_sheet', ticker_symbol)
    else:
        client = YFinanceClient()
        data = client.get_balance_sheet(ticker_symbol)

        # If data is None or empty, use mock data as fallback
        if not data:
            logger.info(f"No balance sheet data from YFinance for {ticker_symbol}, using mock data")
            data = get_mock_data('balance_sheet', ticker_symbol)

    # Transpose the data structure to match frontend expectations
    transposed_data = {}

    for date, values in data.items():
        for item, value in values.items():
            if item not in transposed_data:
                transposed_data[item] = {}
            transposed_data[item][date] = value

    return transposed_data


def get_quarterly_balance_sheet(ticker_symbol):
    """Retrieve quarterly balance sheet data for a given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which the quarterly balance sheet data is requested.

    Returns:
        dict: A dictionary containing the quarterly balance sheet data for the specified ticker.
    """
    if USE_MOCK_DATA:
        data = get_mock_data('balance_sheet', ticker_symbol, quarterly=True)
    else:
        client = YFinanceClient()
        data = client.get_quarterly_balance_sheet(ticker_symbol)

        # If data is None or empty, use mock data as fallback
        if not data:
            logger.info(f"No quarterly balance sheet data from YFinance for {ticker_symbol}, using mock data")
            data = get_mock_data('balance_sheet', ticker_symbol, quarterly=True)

    # Transpose the data structure to match frontend expectations
    transposed_data = {}

    for date, values in data.items():
        for item, value in values.items():
            if item not in transposed_data:
                transposed_data[item] = {}
            transposed_data[item][date] = value

    return transposed_data


def get_cashflow(ticker_symbol):
    """Retrieve annual cashflow data for a given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which the cashflow data is requested.

    Returns:
        dict: A dictionary containing the annual cashflow data for the specified ticker.
    """
    if USE_MOCK_DATA:
        data = get_mock_data('cashflow', ticker_symbol)
    else:
        client = YFinanceClient()
        data = client.get_cashflow(ticker_symbol)

        # If data is None or empty, use mock data as fallback
        if not data:
            logger.info(f"No cashflow data from YFinance for {ticker_symbol}, using mock data")
            data = get_mock_data('cashflow', ticker_symbol)

    # Transpose the data structure to match frontend expectations
    transposed_data = {}

    for date, values in data.items():
        for item, value in values.items():
            if item not in transposed_data:
                transposed_data[item] = {}
            transposed_data[item][date] = value

    return transposed_data


def get_quarterly_cashflow(ticker_symbol):
    """Retrieve quarterly cashflow data for a given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which the quarterly cashflow data is requested.

    Returns:
        dict: A dictionary containing the quarterly cashflow data for the specified ticker.
    """
    if USE_MOCK_DATA:
        data = get_mock_data('cashflow', ticker_symbol, quarterly=True)
    else:
        client = YFinanceClient()
        data = client.get_quarterly_cashflow(ticker_symbol)

        # If data is None or empty, use mock data as fallback
        if not data:
            logger.info(f"No quarterly cashflow data from YFinance for {ticker_symbol}, using mock data")
            data = get_mock_data('cashflow', ticker_symbol, quarterly=True)

    # Transpose the data structure to match frontend expectations
    transposed_data = {}

    for date, values in data.items():
        for item, value in values.items():
            if item not in transposed_data:
                transposed_data[item] = {}
            transposed_data[item][date] = value

    return transposed_data


def get_earnings(ticker_symbol):
    """Retrieve annual earnings (income statement) data for a given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which the annual earnings data is requested.

    Returns:
        dict: A dictionary containing the annual earnings data for the specified ticker.
    """
    if USE_MOCK_DATA:
        data = get_mock_data('earnings', ticker_symbol)
    else:
        client = YFinanceClient()
        data = client.get_earnings(ticker_symbol)

        # If data is None or empty, use mock data as fallback
        if not data:
            logger.info(f"No earnings data from YFinance for {ticker_symbol}, using mock data")
            data = get_mock_data('earnings', ticker_symbol)

    # Transpose the data structure to match frontend expectations
    transposed_data = {}

    for date, values in data.items():
        for item, value in values.items():
            if item not in transposed_data:
                transposed_data[item] = {}
            transposed_data[item][date] = value

    return transposed_data


def get_quarterly_earnings(ticker_symbol):
    """Retrieve quarterly earnings (income statement) data for a given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which the quarterly earnings data is requested.

    Returns:
        dict: A dictionary containing the quarterly earnings data for the specified ticker.
    """
    if USE_MOCK_DATA:
        data = get_mock_data('earnings', ticker_symbol, quarterly=True)
    else:
        client = YFinanceClient()
        data = client.get_quarterly_earnings(ticker_symbol)

        # If data is None or empty, use mock data as fallback
        if not data:
            logger.info(f"No quarterly earnings data from YFinance for {ticker_symbol}, using mock data")
            data = get_mock_data('earnings', ticker_symbol, quarterly=True)

    # Transpose the data structure to match frontend expectations
    transposed_data = {}

    for date, values in data.items():
        for item, value in values.items():
            if item not in transposed_data:
                transposed_data[item] = {}
            transposed_data[item][date] = value

    return transposed_data
