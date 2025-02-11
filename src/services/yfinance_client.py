import yfinance as yf
from django.core.cache import cache
import logging
from services.common_helpers import convert_keys_to_str

logger = logging.getLogger(__name__)

class YFinanceClient:
    def __init__(self, cache_timeout=300):
        """
        cache_timeout: время хранения данных в кэше (в секундах)
        """
        self.cache_timeout = cache_timeout

    def _cache_get_set(self, key, fetch_func):
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
        key = f'yf:info:{ticker_symbol}'
        return self._cache_get_set(key, lambda: convert_keys_to_str(yf.Ticker(ticker_symbol).info))

    def get_history(self, ticker_symbol, start, end, interval="1d"):
        key = f'yf:history:{ticker_symbol}:{start}:{end}:{interval}'
        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            history_df = ticker.history(start=start, end=end, interval=interval)
            if history_df is not None:
                # orient='records' возвращает список словарей, где ключи — имена столбцов (обычно строки)
                return convert_keys_to_str(history_df.to_dict(orient='records'))
            return []
        return self._cache_get_set(key, fetch)

    def get_dividends(self, ticker_symbol):
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
        key = f'yf:splits:{ticker_symbol}'
        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            splits_series = ticker.splits
            if splits_series is not None:
                return convert_keys_to_str(splits_series.to_dict())
            return {}
        return self._cache_get_set(key, fetch)

    def get_recommendations(self, ticker_symbol):
        key = f'yf:recommendations:{ticker_symbol}'
        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            rec_df = ticker.recommendations
            if rec_df is not None:
                return convert_keys_to_str(rec_df.to_dict(orient='records'))
            return []
        return self._cache_get_set(key, fetch)

    def get_calendar(self, ticker_symbol):
        key = f'yf:calendar:{ticker_symbol}'
        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            cal = ticker.calendar
            if cal is not None:
                return convert_keys_to_str(cal.to_dict())
            return {}
        return self._cache_get_set(key, fetch)

    def get_sustainability(self, ticker_symbol):
        key = f'yf:sustainability:{ticker_symbol}'
        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            sus = ticker.sustainability
            if sus is not None:
                return convert_keys_to_str(sus.to_dict())
            return {}
        return self._cache_get_set(key, fetch)

    def get_holders(self, ticker_symbol):
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
        key = f'yf:news:{ticker_symbol}'
        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            news = ticker.news
            if news is not None:
                return convert_keys_to_str(news)
            return []
        return self._cache_get_set(key, fetch)

    # Финансовые данные

    def get_financials(self, ticker_symbol):
        key = f'yf:financials:{ticker_symbol}'
        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            fin = ticker.financials
            if fin is not None:
                return convert_keys_to_str(fin.to_dict())
            return {}
        return self._cache_get_set(key, fetch)

    def get_quarterly_financials(self, ticker_symbol):
        key = f'yf:quarterly_financials:{ticker_symbol}'
        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            qfin = ticker.quarterly_financials
            if qfin is not None:
                return convert_keys_to_str(qfin.to_dict())
            return {}
        return self._cache_get_set(key, fetch)

    def get_balance_sheet(self, ticker_symbol):
        key = f'yf:balance_sheet:{ticker_symbol}'
        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            bs = ticker.balance_sheet
            if bs is not None:
                return convert_keys_to_str(bs.to_dict())
            return {}
        return self._cache_get_set(key, fetch)

    def get_quarterly_balance_sheet(self, ticker_symbol):
        key = f'yf:quarterly_balance_sheet:{ticker_symbol}'
        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            qbs = ticker.quarterly_balance_sheet
            if qbs is not None:
                return convert_keys_to_str(qbs.to_dict())
            return {}
        return self._cache_get_set(key, fetch)

    def get_cashflow(self, ticker_symbol):
        key = f'yf:cashflow:{ticker_symbol}'
        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            cf = ticker.cashflow
            if cf is not None:
                return convert_keys_to_str(cf.to_dict())
            return {}
        return self._cache_get_set(key, fetch)

    def get_quarterly_cashflow(self, ticker_symbol):
        key = f'yf:quarterly_cashflow:{ticker_symbol}'
        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            qcf = ticker.quarterly_cashflow
            if qcf is not None:
                return convert_keys_to_str(qcf.to_dict())
            return {}
        return self._cache_get_set(key, fetch)

    def get_earnings(self, ticker_symbol):
        """
        Получает годовой отчёт о доходах через Ticker.income_stmt.
        Вместо устаревшего Ticker.earnings теперь используем income_stmt.
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
        """
        Получает квартальные данные отчёта о доходах через Ticker.quarterly_income_stmt.
        Вместо устаревшего Ticker.quarterly_earnings теперь используем quarterly_income_stmt.
        """
        key = f'yf:quarterly_earnings:{ticker_symbol}'

        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            q_income_stmt = ticker.quarterly_income_stmt
            if q_income_stmt is not None:
                return convert_keys_to_str(q_income_stmt.to_dict())
            return {}

        return self._cache_get_set(key, fetch)
    # Опционные данные

    def get_options_dates(self, ticker_symbol):
        key = f'yf:options_dates:{ticker_symbol}'
        def fetch():
            ticker = yf.Ticker(ticker_symbol)
            options = ticker.options
            if options is not None:
                return options  # Обычно список дат в виде строк
            return []
        return self._cache_get_set(key, fetch)

    def get_option_chain(self, ticker_symbol, date):
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
