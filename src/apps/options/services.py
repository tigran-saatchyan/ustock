from services.yfinance_client import YFinanceClient

def get_options_dates(ticker_symbol):
    """Retrieve options expiration dates for the given ticker.

    Args:
        ticker_symbol (str): The ticker symbol for which to retrieve options dates.

    Returns:
        list: A list of available options expiration dates for the ticker.
    """
    client = YFinanceClient()
    return client.get_options_dates(ticker_symbol)

def get_option_chain(ticker_symbol, date):
    """Retrieve the options chain for the given ticker and expiration date.

    Args:
        ticker_symbol (str): The ticker symbol for which to retrieve the options chain.
        date (str): The expiration date (in "YYYY-MM-DD" format) for which the options chain is requested.

    Returns:
        dict: A dictionary containing the options chain data, typically including 'calls' and 'puts'.
    """
    client = YFinanceClient()
    return client.get_option_chain(ticker_symbol, date)
