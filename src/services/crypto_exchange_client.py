import os
import logging
from abc import ABC, abstractmethod
from django.core.cache import cache

logger = logging.getLogger(__name__)

class CryptoExchangeClient(ABC):
    """Base abstract class for crypto exchange clients.
    
    This class defines the interface that all crypto exchange clients must implement.
    It provides common functionality like caching and error handling.
    """
    
    def __init__(self, api_key=None, api_secret=None, base_url=None, cache_timeout=300):
        """Initialize the crypto exchange client.
        
        Args:
            api_key (str, optional): API key for the exchange. Defaults to None.
            api_secret (str, optional): API secret for the exchange. Defaults to None.
            base_url (str, optional): Base URL for the exchange API. Defaults to None.
            cache_timeout (int, optional): Cache timeout in seconds. Defaults to 300.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
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
    
    @abstractmethod
    def get_account_info(self):
        """Get account information including balances.
        
        Returns:
            dict: Account information including balances.
        """
        pass
    
    @abstractmethod
    def get_ticker_price(self, symbol):
        """Get the current price for a symbol.
        
        Args:
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            
        Returns:
            dict: Current price information.
        """
        pass
    
    @abstractmethod
    def get_order_book(self, symbol, limit=20):
        """Get the order book for a symbol.
        
        Args:
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            limit (int, optional): The number of orders to return. Defaults to 20.
            
        Returns:
            dict: Order book information.
        """
        pass
    
    @abstractmethod
    def get_recent_trades(self, symbol, limit=20):
        """Get recent trades for a symbol.
        
        Args:
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            limit (int, optional): The number of trades to return. Defaults to 20.
            
        Returns:
            list: Recent trades.
        """
        pass
    
    @abstractmethod
    def create_order(self, symbol, side, order_type, quantity, price=None):
        """Create a new order.
        
        Args:
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            side (str): Order side (BUY or SELL).
            order_type (str): Order type (LIMIT, MARKET, etc.).
            quantity (float): Order quantity.
            price (float, optional): Order price (required for LIMIT orders). Defaults to None.
            
        Returns:
            dict: Order information.
        """
        pass
    
    @abstractmethod
    def get_order(self, symbol, order_id):
        """Get order information.
        
        Args:
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            order_id (str): The order ID.
            
        Returns:
            dict: Order information.
        """
        pass
    
    @abstractmethod
    def cancel_order(self, symbol, order_id):
        """Cancel an order.
        
        Args:
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            order_id (str): The order ID.
            
        Returns:
            dict: Cancellation result.
        """
        pass
    
    @abstractmethod
    def get_open_orders(self, symbol=None):
        """Get open orders.
        
        Args:
            symbol (str, optional): The trading pair symbol (e.g., 'BTCUSDT'). Defaults to None.
            
        Returns:
            list: Open orders.
        """
        pass