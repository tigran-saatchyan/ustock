import os
import logging
import hmac
import hashlib
import time
import requests
from urllib.parse import urlencode
from .crypto_exchange_client import CryptoExchangeClient

logger = logging.getLogger(__name__)

class BinanceClient(CryptoExchangeClient):
    """Client for accessing Binance API.
    
    This client implements the CryptoExchangeClient interface for Binance.
    """
    
    def __init__(self, api_key=None, api_secret=None, base_url=None, cache_timeout=300):
        """Initialize the Binance client.
        
        Args:
            api_key (str, optional): Binance API key. Defaults to None.
            api_secret (str, optional): Binance API secret. Defaults to None.
            base_url (str, optional): Binance API base URL. Defaults to None.
            cache_timeout (int, optional): Cache timeout in seconds. Defaults to 300.
        """
        # Use environment variables if not provided
        api_key = api_key or os.environ.get('TEST_SPOT_API_KEY')
        api_secret = api_secret or os.environ.get('TEST_SPOT_API_SECRET')
        base_url = base_url or os.environ.get('TEST_SPOT_BASE_URL', 'https://testnet.binance.vision')
        
        super().__init__(api_key, api_secret, base_url, cache_timeout)
    
    def _generate_signature(self, data):
        """Generate HMAC SHA256 signature for Binance API.
        
        Args:
            data (dict): Data to sign.
            
        Returns:
            str: HMAC SHA256 signature.
        """
        query_string = urlencode(data)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _make_request(self, method, endpoint, params=None, signed=False):
        """Make a request to the Binance API.
        
        Args:
            method (str): HTTP method (GET, POST, DELETE).
            endpoint (str): API endpoint.
            params (dict, optional): Request parameters. Defaults to None.
            signed (bool, optional): Whether the request needs to be signed. Defaults to False.
            
        Returns:
            dict: Response data.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {'X-MBX-APIKEY': self.api_key} if self.api_key else {}
        
        if params is None:
            params = {}
        
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, headers=headers, params=params)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to {url}: {e}")
            raise
    
    def get_account_info(self):
        """Get account information including balances.
        
        Returns:
            dict: Account information including balances.
        """
        key = f'binance:account_info:{self.api_key}'
        
        def fetch():
            return self._make_request('GET', '/api/v3/account', signed=True)
        
        return self._cache_get_set(key, fetch)
    
    def get_ticker_price(self, symbol):
        """Get the current price for a symbol.
        
        Args:
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            
        Returns:
            dict: Current price information.
        """
        key = f'binance:ticker_price:{symbol}'
        
        def fetch():
            return self._make_request('GET', '/api/v3/ticker/price', {'symbol': symbol})
        
        return self._cache_get_set(key, fetch)
    
    def get_order_book(self, symbol, limit=20):
        """Get the order book for a symbol.
        
        Args:
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            limit (int, optional): The number of orders to return. Defaults to 20.
            
        Returns:
            dict: Order book information.
        """
        key = f'binance:order_book:{symbol}:{limit}'
        
        def fetch():
            return self._make_request('GET', '/api/v3/depth', {'symbol': symbol, 'limit': limit})
        
        return self._cache_get_set(key, fetch)
    
    def get_recent_trades(self, symbol, limit=20):
        """Get recent trades for a symbol.
        
        Args:
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            limit (int, optional): The number of trades to return. Defaults to 20.
            
        Returns:
            list: Recent trades.
        """
        key = f'binance:recent_trades:{symbol}:{limit}'
        
        def fetch():
            return self._make_request('GET', '/api/v3/trades', {'symbol': symbol, 'limit': limit})
        
        return self._cache_get_set(key, fetch)
    
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
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
        }
        
        if order_type == 'LIMIT':
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            params['price'] = price
            params['timeInForce'] = 'GTC'  # Good Till Cancelled
        
        return self._make_request('POST', '/api/v3/order', params, signed=True)
    
    def get_order(self, symbol, order_id):
        """Get order information.
        
        Args:
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            order_id (str): The order ID.
            
        Returns:
            dict: Order information.
        """
        params = {
            'symbol': symbol,
            'orderId': order_id,
        }
        
        return self._make_request('GET', '/api/v3/order', params, signed=True)
    
    def cancel_order(self, symbol, order_id):
        """Cancel an order.
        
        Args:
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            order_id (str): The order ID.
            
        Returns:
            dict: Cancellation result.
        """
        params = {
            'symbol': symbol,
            'orderId': order_id,
        }
        
        return self._make_request('DELETE', '/api/v3/order', params, signed=True)
    
    def get_open_orders(self, symbol=None):
        """Get open orders.
        
        Args:
            symbol (str, optional): The trading pair symbol (e.g., 'BTCUSDT'). Defaults to None.
            
        Returns:
            list: Open orders.
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        
        key = f'binance:open_orders:{self.api_key}:{symbol or "all"}'
        
        def fetch():
            return self._make_request('GET', '/api/v3/openOrders', params, signed=True)
        
        return self._cache_get_set(key, fetch)
    
    def get_exchange_info(self):
        """Get exchange information.
        
        Returns:
            dict: Exchange information.
        """
        key = 'binance:exchange_info'
        
        def fetch():
            return self._make_request('GET', '/api/v3/exchangeInfo')
        
        return self._cache_get_set(key, fetch)
    
    def get_all_tickers(self):
        """Get all ticker prices.
        
        Returns:
            list: All ticker prices.
        """
        key = 'binance:all_tickers'
        
        def fetch():
            return self._make_request('GET', '/api/v3/ticker/price')
        
        return self._cache_get_set(key, fetch)