import logging
from django.conf import settings
from services.binance_client import BinanceClient
from apps.personal_finance.models import CryptoExchangeAPI

logger = logging.getLogger(__name__)

class CryptoTradingService:
    """Service for crypto trading functionality.
    
    This service provides methods for interacting with crypto exchanges
    and retrieving crypto-related data.
    """
    
    @staticmethod
    def get_client_for_user(user, exchange='binance'):
        """Get a crypto exchange client for a user.
        
        Args:
            user: The user to get the client for.
            exchange (str, optional): The exchange to get the client for. Defaults to 'binance'.
            
        Returns:
            CryptoExchangeClient: A client for the specified exchange.
        """
        try:
            api_keys = CryptoExchangeAPI.objects.get(user=user, exchange=exchange, is_active=True)
            
            if exchange == 'binance':
                return BinanceClient(api_key=api_keys.api_key, api_secret=api_keys.api_secret)
            else:
                logger.error(f"Unsupported exchange: {exchange}")
                return None
        except CryptoExchangeAPI.DoesNotExist:
            logger.info(f"No API keys found for user {user.username} and exchange {exchange}")
            
            # If no API keys are found, use the default ones from environment variables
            if exchange == 'binance':
                return BinanceClient()
            else:
                logger.error(f"Unsupported exchange: {exchange}")
                return None
    
    @staticmethod
    def get_account_balance(user, exchange='binance'):
        """Get the account balance for a user.
        
        Args:
            user: The user to get the balance for.
            exchange (str, optional): The exchange to get the balance from. Defaults to 'binance'.
            
        Returns:
            dict: Account balance information.
        """
        client = CryptoTradingService.get_client_for_user(user, exchange)
        if client:
            try:
                account_info = client.get_account_info()
                
                # Process the account info to extract balances
                balances = []
                if 'balances' in account_info:
                    for balance in account_info['balances']:
                        # Only include assets with non-zero balance
                        free = float(balance['free'])
                        locked = float(balance['locked'])
                        if free > 0 or locked > 0:
                            # Get current price for the asset
                            price = 0
                            try:
                                if balance['asset'] != 'USDT':  # Skip USDT as it's the base currency
                                    symbol = f"{balance['asset']}USDT"
                                    price_info = client.get_ticker_price(symbol)
                                    price = float(price_info['price'])
                                else:
                                    price = 1.0  # USDT price is 1 USDT
                            except Exception as e:
                                logger.error(f"Error getting price for {balance['asset']}: {e}")
                            
                            balances.append({
                                'asset': balance['asset'],
                                'free': free,
                                'locked': locked,
                                'total': free + locked,
                                'price_usdt': price,
                                'value_usdt': (free + locked) * price
                            })
                
                # Sort balances by value (descending)
                balances.sort(key=lambda x: x['value_usdt'], reverse=True)
                
                # Calculate total value
                total_value = sum(balance['value_usdt'] for balance in balances)
                
                return {
                    'balances': balances,
                    'total_value_usdt': total_value
                }
            except Exception as e:
                logger.error(f"Error getting account balance: {e}")
                return {'error': str(e)}
        else:
            return {'error': 'No client available'}
    
    @staticmethod
    def get_ticker_price(symbol, user=None, exchange='binance'):
        """Get the current price for a symbol.
        
        Args:
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            user (optional): The user to get the price for. If None, uses default client.
            exchange (str, optional): The exchange to get the price from. Defaults to 'binance'.
            
        Returns:
            dict: Current price information.
        """
        client = BinanceClient()  # Use default client for public endpoints
        if user:
            user_client = CryptoTradingService.get_client_for_user(user, exchange)
            if user_client:
                client = user_client
        
        try:
            return client.get_ticker_price(symbol)
        except Exception as e:
            logger.error(f"Error getting ticker price for {symbol}: {e}")
            return {'error': str(e)}
    
    @staticmethod
    def get_order_book(symbol, limit=20, user=None, exchange='binance'):
        """Get the order book for a symbol.
        
        Args:
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            limit (int, optional): The number of orders to return. Defaults to 20.
            user (optional): The user to get the order book for. If None, uses default client.
            exchange (str, optional): The exchange to get the order book from. Defaults to 'binance'.
            
        Returns:
            dict: Order book information.
        """
        client = BinanceClient()  # Use default client for public endpoints
        if user:
            user_client = CryptoTradingService.get_client_for_user(user, exchange)
            if user_client:
                client = user_client
        
        try:
            return client.get_order_book(symbol, limit)
        except Exception as e:
            logger.error(f"Error getting order book for {symbol}: {e}")
            return {'error': str(e)}
    
    @staticmethod
    def create_order(user, symbol, side, order_type, quantity, price=None, exchange='binance'):
        """Create a new order.
        
        Args:
            user: The user creating the order.
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            side (str): Order side (BUY or SELL).
            order_type (str): Order type (LIMIT, MARKET, etc.).
            quantity (float): Order quantity.
            price (float, optional): Order price (required for LIMIT orders). Defaults to None.
            exchange (str, optional): The exchange to create the order on. Defaults to 'binance'.
            
        Returns:
            dict: Order information.
        """
        client = CryptoTradingService.get_client_for_user(user, exchange)
        if client:
            try:
                return client.create_order(symbol, side, order_type, quantity, price)
            except Exception as e:
                logger.error(f"Error creating order: {e}")
                return {'error': str(e)}
        else:
            return {'error': 'No client available'}
    
    @staticmethod
    def get_open_orders(user, symbol=None, exchange='binance'):
        """Get open orders for a user.
        
        Args:
            user: The user to get open orders for.
            symbol (str, optional): The trading pair symbol (e.g., 'BTCUSDT'). Defaults to None.
            exchange (str, optional): The exchange to get open orders from. Defaults to 'binance'.
            
        Returns:
            list: Open orders.
        """
        client = CryptoTradingService.get_client_for_user(user, exchange)
        if client:
            try:
                return client.get_open_orders(symbol)
            except Exception as e:
                logger.error(f"Error getting open orders: {e}")
                return {'error': str(e)}
        else:
            return {'error': 'No client available'}
    
    @staticmethod
    def cancel_order(user, symbol, order_id, exchange='binance'):
        """Cancel an order.
        
        Args:
            user: The user canceling the order.
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            order_id (str): The order ID.
            exchange (str, optional): The exchange to cancel the order on. Defaults to 'binance'.
            
        Returns:
            dict: Cancellation result.
        """
        client = CryptoTradingService.get_client_for_user(user, exchange)
        if client:
            try:
                return client.cancel_order(symbol, order_id)
            except Exception as e:
                logger.error(f"Error canceling order: {e}")
                return {'error': str(e)}
        else:
            return {'error': 'No client available'}
    
    @staticmethod
    def get_exchange_info(exchange='binance'):
        """Get exchange information.
        
        Args:
            exchange (str, optional): The exchange to get information for. Defaults to 'binance'.
            
        Returns:
            dict: Exchange information.
        """
        client = BinanceClient()  # Use default client for public endpoints
        
        try:
            return client.get_exchange_info()
        except Exception as e:
            logger.error(f"Error getting exchange info: {e}")
            return {'error': str(e)}
    
    @staticmethod
    def get_all_tickers(exchange='binance'):
        """Get all ticker prices.
        
        Args:
            exchange (str, optional): The exchange to get ticker prices from. Defaults to 'binance'.
            
        Returns:
            list: All ticker prices.
        """
        client = BinanceClient()  # Use default client for public endpoints
        
        try:
            return client.get_all_tickers()
        except Exception as e:
            logger.error(f"Error getting all tickers: {e}")
            return {'error': str(e)}