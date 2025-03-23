import yfinance as yf
from django.core.cache import cache
import logging
from services.common_helpers import convert_keys_to_str

logger = logging.getLogger(__name__)


class YFinanceClient:
    """Client for accessing financial data via the yFinance API.

    This client wraps the yfinance.Ticker object and provides methods to retrieve
    various types of data (ticker info, historical prices, dividends, splits, financial
    statements, options data, etc.) with caching support.
    """

    def __init__(self, cache_timeout=300):
        """Initialize the YFinanceClient instance.

        Args:
            cache_timeout (int, optional): Cache timeout in seconds. Defaults to 300.
        """
        self.cache_timeout = cache_timeout

    def _cache_get_set(self, key, fetch_func):
        """Retrieve data from cache or fetch and cache it.

        Args:
            key (str): The cache key.
            fetch_func (callable): A function that fetches the data if it's not in cache.

        Returns:
            Any: The data fetched from cache or obtained by executing fetch_func.
        """
        data = cache.get(key)
        if data is None:
            try:
                data = fetch_func()
                cache.set(key, data, self.cache_timeout)
            except Exception as e:
                logger.error(f"Error for key {key}: {e}")
                data = None
        return data

    def get_ticker_info(self, ticker_symbol):
        """Retrieve general ticker information.

        Args:
            ticker_symbol (str): The ticker symbol to retrieve information for.

        Returns:
            dict: A dictionary containing the ticker symbol and its related information.
        """
        key = f'yf:info:{ticker_symbol}'
        return self._cache_get_set(key, lambda: convert_keys_to_str(yf.Ticker(ticker_symbol).info))

    def get_history(self, ticker_symbol, start, end, interval="1d"):
        """Retrieve historical price data for the given ticker.

        Args:
            ticker_symbol (str): The ticker symbol.
            start (str): The start date (YYYY-MM-DD).
            end (str): The end date (YYYY-MM-DD).
            interval (str, optional): The data interval (e.g., '1d', '1wk', '1mo'). Defaults to "1d".

        Returns:
            list: A list of dictionaries representing historical price records.
        """
        key = f'yf:history:{ticker_symbol}:{start}:{end}:{interval}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            history_df = ticker.history(start=start, end=end, interval=interval)
            if history_df is not None and not history_df.empty:
                # Fill NaN values with None to properly handle them in JSON serialization
                history_df = history_df.fillna(None)
                
                # Reset index to make the Date a column
                history_df = history_df.reset_index()
                
                # Convert datetime objects to ISO format strings for JSON serialization
                if 'Date' in history_df.columns:
                    history_df['Date'] = history_df['Date'].dt.strftime('%Y-%m-%d')
                
                # 'orient="records"' returns a list of dictionaries with column names as keys.
                result = convert_keys_to_str(history_df.to_dict(orient='records'))
                
                # Normalize the data format to match frontend expectations
                normalized_result = []
                for item in result:
                    normalized_item = {
                        'date': item.get('Date'),
                        'open': item.get('Open'),
                        'high': item.get('High'),
                        'low': item.get('Low'),
                        'close': item.get('Close'),
                        'volume': item.get('Volume')
                    }
                    # Remove any None values
                    normalized_result.append({k: v for k, v in normalized_item.items() if v is not None})
                
                result = normalized_result
                
                # Log some sample data for debugging
                logger.info(f"Retrieved {len(result)} history records for {ticker_symbol}")
                if result and len(result) > 0:
                    logger.info(f"Sample data point: {result[0]}")
                
                return result
            return []

        return self._cache_get_set(key, fetch)

    def get_dividends(self, ticker_symbol):
        """Retrieve dividend data for the given ticker.

        Args:
            ticker_symbol (str): The ticker symbol.

        Returns:
            dict: A dictionary containing dividend data.
        """
        key = f'yf:dividends:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            div_series = ticker.dividends
            if div_series is not None:
                raw = div_series.to_dict()
                return convert_keys_to_str(raw)
            return {}

        return self._cache_get_set(key, fetch)

    def get_splits(self, ticker_symbol):
        """Retrieve stock splits data for the given ticker.

        Args:
            ticker_symbol (str): The ticker symbol.

        Returns:
            dict: A dictionary containing stock splits data.
        """
        key = f'yf:splits:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            splits_series = ticker.splits
            if splits_series is not None:
                return convert_keys_to_str(splits_series.to_dict())
            return {}

        return self._cache_get_set(key, fetch)

    def get_recommendations(self, ticker_symbol):
        """Retrieve analyst recommendations for the given ticker.

        Args:
            ticker_symbol (str): The ticker symbol.

        Returns:
            list: A list of dictionaries representing analyst recommendations.
        """
        key = f'yf:recommendations:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            rec_df = ticker.recommendations
            if rec_df is not None:
                return convert_keys_to_str(rec_df.to_dict(orient='records'))
            return []

        return self._cache_get_set(key, fetch)

    def get_calendar(self, ticker_symbol):
        """Retrieve the event calendar for the given ticker.

        Args:
            ticker_symbol (str): The ticker symbol.

        Returns:
            dict: A dictionary containing calendar data (e.g., earnings dates, events).
        """
        key = f'yf:calendar:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            cal = ticker.calendar
            if cal is not None:
                return convert_keys_to_str(cal.to_dict())
            return {}

        return self._cache_get_set(key, fetch)

    def get_sustainability(self, ticker_symbol):
        """Retrieve ESG/sustainability data for the given ticker.

        Args:
            ticker_symbol (str): The ticker symbol.

        Returns:
            dict: A dictionary containing sustainability (ESG) metrics.
        """
        key = f'yf:sustainability:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            sus = ticker.sustainability
            if sus is not None:
                return convert_keys_to_str(sus.to_dict())
            return {}

        return self._cache_get_set(key, fetch)

    def get_holders(self, ticker_symbol):
        """Retrieve holders information for the given ticker.

        Args:
            ticker_symbol (str): The ticker symbol.

        Returns:
            dict: A dictionary with keys 'institutional_holders', 'major_holders', and 'mutualfund_holders',
                  each containing a list of dictionaries representing holder data.
        """
        key = f'yf:holders:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            institutional = ticker.institutional_holders
            major = ticker.major_holders
            mutualfund = ticker.mutualfund_holders
            return convert_keys_to_str({
                'institutional_holders': institutional.to_dict(orient='records') if institutional is not None else [],
                'major_holders': major.to_dict(orient='records') if major is not None else [],
                'mutualfund_holders': mutualfund.to_dict(orient='records') if mutualfund is not None else [],
            })

        return self._cache_get_set(key, fetch)

    def get_news(self, ticker_symbol):
        """Retrieve news data for the given ticker.

        Args:
            ticker_symbol (str): The ticker symbol.

        Returns:
            list: A list containing news articles and related information.
        """
        key = f'yf:news:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            news = ticker.news
            if news is not None:
                return convert_keys_to_str(news)
            return []

        return self._cache_get_set(key, fetch)

    # Financial Data

    def get_financials(self, ticker_symbol):
        """Retrieve annual financial statements for the given ticker.

        Args:
            ticker_symbol (str): The ticker symbol.

        Returns:
            dict: A dictionary containing annual financial data.
        """
        key = f'yf:financials:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            fin = ticker.financials
            if fin is not None:
                return convert_keys_to_str(fin.to_dict())
            return {}

        return self._cache_get_set(key, fetch)

    def get_quarterly_financials(self, ticker_symbol):
        """Retrieve quarterly financial statements for the given ticker.

        Args:
            ticker_symbol (str): The ticker symbol.

        Returns:
            dict: A dictionary containing quarterly financial data.
        """
        key = f'yf:quarterly_financials:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            qfin = ticker.quarterly_financials
            if qfin is not None:
                return convert_keys_to_str(qfin.to_dict())
            return {}

        return self._cache_get_set(key, fetch)

    def get_balance_sheet(self, ticker_symbol):
        """Retrieve the annual balance sheet for the given ticker.

        Args:
            ticker_symbol (str): The ticker symbol.

        Returns:
            dict: A dictionary containing balance sheet data.
        """
        key = f'yf:balance_sheet:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            bs = ticker.balance_sheet
            if bs is not None:
                return convert_keys_to_str(bs.to_dict())
            return {}

        return self._cache_get_set(key, fetch)

    def get_quarterly_balance_sheet(self, ticker_symbol):
        """Retrieve the quarterly balance sheet for the given ticker.

        Args:
            ticker_symbol (str): The ticker symbol.

        Returns:
            dict: A dictionary containing quarterly balance sheet data.
        """
        key = f'yf:quarterly_balance_sheet:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            qbs = ticker.quarterly_balance_sheet
            if qbs is not None:
                return convert_keys_to_str(qbs.to_dict())
            return {}

        return self._cache_get_set(key, fetch)

    def get_cashflow(self, ticker_symbol):
        """Retrieve the annual cashflow statement for the given ticker.

        Args:
            ticker_symbol (str): The ticker symbol.

        Returns:
            dict: A dictionary containing annual cashflow data.
        """
        key = f'yf:cashflow:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            cf = ticker.cashflow
            if cf is not None:
                return convert_keys_to_str(cf.to_dict())
            return {}

        return self._cache_get_set(key, fetch)

    def get_quarterly_cashflow(self, ticker_symbol):
        """Retrieve the quarterly cashflow statement for the given ticker.

        Args:
            ticker_symbol (str): The ticker symbol.

        Returns:
            dict: A dictionary containing quarterly cashflow data.
        """
        key = f'yf:quarterly_cashflow:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            qcf = ticker.quarterly_cashflow
            if qcf is not None:
                return convert_keys_to_str(qcf.to_dict())
            return {}

        return self._cache_get_set(key, fetch)

    def get_earnings(self, ticker_symbol):
        """Retrieve the annual income statement for the given ticker.

        This method retrieves the income statement via Ticker.income_stmt. Note that
        the deprecated Ticker.earnings is no longer used.

        Args:
            ticker_symbol (str): The ticker symbol.

        Returns:
            dict: A dictionary containing the annual income statement data.
        """
        key = f'yf:earnings:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            income_stmt = ticker.income_stmt
            if income_stmt is not None:
                return convert_keys_to_str(income_stmt.to_dict())
            return {}

        return self._cache_get_set(key, fetch)

    def get_quarterly_earnings(self, ticker_symbol):
        """Retrieve the quarterly income statement for the given ticker.

        This method retrieves the income statement via Ticker.quarterly_income_stmt.
        The deprecated Ticker.quarterly_earnings is no longer used.

        Args:
            ticker_symbol (str): The ticker symbol.

        Returns:
            dict: A dictionary containing the quarterly income statement data.
        """
        key = f'yf:quarterly_earnings:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            q_income_stmt = ticker.quarterly_income_stmt
            if q_income_stmt is not None:
                return convert_keys_to_str(q_income_stmt.to_dict())
            return {}

        return self._cache_get_set(key, fetch)

    # Options Data

    def get_options_dates(self, ticker_symbol):
        """Retrieve available options expiration dates for the given ticker.

        Args:
            ticker_symbol (str): The ticker symbol.

        Returns:
            list: A list of expiration dates (as strings).
        """
        key = f'yf:options_dates:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            options = ticker.options
            if options is not None:
                return options  # Typically a list of date strings
            return []

        return self._cache_get_set(key, fetch)

    def get_option_chain(self, ticker_symbol, date):
        """Retrieve the option chain for the given ticker and expiration date.

        Args:
            ticker_symbol (str): The ticker symbol.
            date (str): The expiration date in 'YYYY-MM-DD' format.

        Returns:
            dict: A dictionary containing two keys, 'calls' and 'puts', each being a list
                  of dictionaries representing the options chain data.
        """
        key = f'yf:option_chain:{ticker_symbol}:{date}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            chain = ticker.option_chain(date)
            calls = chain.calls.to_dict(orient='records') if chain and chain.calls is not None else []
            puts = chain.puts.to_dict(orient='records') if chain and chain.puts is not None else []
            return convert_keys_to_str({
                'calls': calls,
                'puts': puts,
            })

        return self._cache_get_set(key, fetch)
