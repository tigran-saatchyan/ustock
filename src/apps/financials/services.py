from services.yfinance_client import YFinanceClient

def get_financials(ticker_symbol):
    """Retrieve annual financial data for a given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which financial data is requested.

    Returns:
        dict: A dictionary containing the annual financial data for the specified ticker.
    """
    client = YFinanceClient()
    return client.get_financials(ticker_symbol)


def get_quarterly_financials(ticker_symbol):
    """Retrieve quarterly financial data for a given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which quarterly financial data is requested.

    Returns:
        dict: A dictionary containing the quarterly financial data for the specified ticker.
    """
    client = YFinanceClient()
    return client.get_quarterly_financials(ticker_symbol)


def get_balance_sheet(ticker_symbol):
    """Retrieve annual balance sheet data for a given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which the balance sheet data is requested.

    Returns:
        dict: A dictionary containing the annual balance sheet data for the specified ticker.
    """
    client = YFinanceClient()
    return client.get_balance_sheet(ticker_symbol)


def get_quarterly_balance_sheet(ticker_symbol):
    """Retrieve quarterly balance sheet data for a given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which the quarterly balance sheet data is requested.

    Returns:
        dict: A dictionary containing the quarterly balance sheet data for the specified ticker.
    """
    client = YFinanceClient()
    return client.get_quarterly_balance_sheet(ticker_symbol)


def get_cashflow(ticker_symbol):
    """Retrieve annual cashflow data for a given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which the cashflow data is requested.

    Returns:
        dict: A dictionary containing the annual cashflow data for the specified ticker.
    """
    client = YFinanceClient()
    return client.get_cashflow(ticker_symbol)


def get_quarterly_cashflow(ticker_symbol):
    """Retrieve quarterly cashflow data for a given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which the quarterly cashflow data is requested.

    Returns:
        dict: A dictionary containing the quarterly cashflow data for the specified ticker.
    """
    client = YFinanceClient()
    return client.get_quarterly_cashflow(ticker_symbol)


def get_earnings(ticker_symbol):
    """Retrieve annual earnings (income statement) data for a given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which the annual earnings data is requested.

    Returns:
        dict: A dictionary containing the annual earnings data for the specified ticker.
    """
    client = YFinanceClient()
    return client.get_earnings(ticker_symbol)


def get_quarterly_earnings(ticker_symbol):
    """Retrieve quarterly earnings (income statement) data for a given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which the quarterly earnings data is requested.

    Returns:
        dict: A dictionary containing the quarterly earnings data for the specified ticker.
    """
    client = YFinanceClient()
    return client.get_quarterly_earnings(ticker_symbol)
