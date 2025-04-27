from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .crypto_services import CryptoTradingService
from apps.personal_finance.models import CryptoExchangeAPI
from django.shortcuts import get_object_or_404

class CryptoAccountBalanceView(APIView):
    """API view for retrieving crypto account balance.
    
    This endpoint fetches the account balance for the authenticated user
    from the specified exchange.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, exchange='binance'):
        """Handle GET requests for account balance.
        
        Args:
            request (Request): The HTTP request object.
            exchange (str, optional): The exchange to get the balance from. Defaults to 'binance'.
            
        Returns:
            Response: A REST framework Response object containing the account balance.
        """
        balance = CryptoTradingService.get_account_balance(request.user, exchange)
        return Response(balance, status=status.HTTP_200_OK)

class CryptoTickerPriceView(APIView):
    """API view for retrieving crypto ticker price.
    
    This endpoint fetches the current price for a symbol from the specified exchange.
    """
    
    def get(self, request, symbol, exchange='binance'):
        """Handle GET requests for ticker price.
        
        Args:
            request (Request): The HTTP request object.
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            exchange (str, optional): The exchange to get the price from. Defaults to 'binance'.
            
        Returns:
            Response: A REST framework Response object containing the ticker price.
        """
        price = CryptoTradingService.get_ticker_price(symbol, request.user if request.user.is_authenticated else None, exchange)
        return Response(price, status=status.HTTP_200_OK)

class CryptoOrderBookView(APIView):
    """API view for retrieving crypto order book.
    
    This endpoint fetches the order book for a symbol from the specified exchange.
    """
    
    def get(self, request, symbol, exchange='binance'):
        """Handle GET requests for order book.
        
        Args:
            request (Request): The HTTP request object.
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            exchange (str, optional): The exchange to get the order book from. Defaults to 'binance'.
            
        Returns:
            Response: A REST framework Response object containing the order book.
        """
        limit = request.query_params.get('limit', 20)
        order_book = CryptoTradingService.get_order_book(
            symbol, 
            limit=int(limit), 
            user=request.user if request.user.is_authenticated else None, 
            exchange=exchange
        )
        return Response(order_book, status=status.HTTP_200_OK)

class CryptoCreateOrderView(APIView):
    """API view for creating crypto orders.
    
    This endpoint creates a new order on the specified exchange.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, exchange='binance'):
        """Handle POST requests for creating orders.
        
        Args:
            request (Request): The HTTP request object.
            exchange (str, optional): The exchange to create the order on. Defaults to 'binance'.
            
        Returns:
            Response: A REST framework Response object containing the order information.
        """
        symbol = request.data.get('symbol')
        side = request.data.get('side')
        order_type = request.data.get('type')
        quantity = request.data.get('quantity')
        price = request.data.get('price')
        
        if not all([symbol, side, order_type, quantity]):
            return Response(
                {'error': 'Missing required parameters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order = CryptoTradingService.create_order(
            request.user, 
            symbol, 
            side, 
            order_type, 
            quantity, 
            price, 
            exchange
        )
        return Response(order, status=status.HTTP_201_CREATED)

class CryptoOpenOrdersView(APIView):
    """API view for retrieving open crypto orders.
    
    This endpoint fetches open orders for the authenticated user
    from the specified exchange.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, exchange='binance'):
        """Handle GET requests for open orders.
        
        Args:
            request (Request): The HTTP request object.
            exchange (str, optional): The exchange to get open orders from. Defaults to 'binance'.
            
        Returns:
            Response: A REST framework Response object containing the open orders.
        """
        symbol = request.query_params.get('symbol')
        orders = CryptoTradingService.get_open_orders(request.user, symbol, exchange)
        return Response(orders, status=status.HTTP_200_OK)

class CryptoCancelOrderView(APIView):
    """API view for canceling crypto orders.
    
    This endpoint cancels an order on the specified exchange.
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, symbol, order_id, exchange='binance'):
        """Handle DELETE requests for canceling orders.
        
        Args:
            request (Request): The HTTP request object.
            symbol (str): The trading pair symbol (e.g., 'BTCUSDT').
            order_id (str): The order ID.
            exchange (str, optional): The exchange to cancel the order on. Defaults to 'binance'.
            
        Returns:
            Response: A REST framework Response object containing the cancellation result.
        """
        result = CryptoTradingService.cancel_order(request.user, symbol, order_id, exchange)
        return Response(result, status=status.HTTP_200_OK)

class CryptoExchangeInfoView(APIView):
    """API view for retrieving crypto exchange information.
    
    This endpoint fetches exchange information from the specified exchange.
    """
    
    def get(self, request, exchange='binance'):
        """Handle GET requests for exchange information.
        
        Args:
            request (Request): The HTTP request object.
            exchange (str, optional): The exchange to get information for. Defaults to 'binance'.
            
        Returns:
            Response: A REST framework Response object containing the exchange information.
        """
        info = CryptoTradingService.get_exchange_info(exchange)
        return Response(info, status=status.HTTP_200_OK)

class CryptoAllTickersView(APIView):
    """API view for retrieving all crypto ticker prices.
    
    This endpoint fetches all ticker prices from the specified exchange.
    """
    
    def get(self, request, exchange='binance'):
        """Handle GET requests for all ticker prices.
        
        Args:
            request (Request): The HTTP request object.
            exchange (str, optional): The exchange to get ticker prices from. Defaults to 'binance'.
            
        Returns:
            Response: A REST framework Response object containing all ticker prices.
        """
        tickers = CryptoTradingService.get_all_tickers(exchange)
        return Response(tickers, status=status.HTTP_200_OK)

class CryptoAPIKeysView(APIView):
    """API view for managing crypto API keys.
    
    This endpoint allows users to view, create, update, and delete their API keys
    for different exchanges.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, exchange=None):
        """Handle GET requests for API keys.
        
        Args:
            request (Request): The HTTP request object.
            exchange (str, optional): The exchange to get API keys for. Defaults to None.
            
        Returns:
            Response: A REST framework Response object containing the API keys.
        """
        if exchange:
            try:
                api_key = CryptoExchangeAPI.objects.get(user=request.user, exchange=exchange)
                return Response({
                    'exchange': api_key.exchange,
                    'is_active': api_key.is_active,
                    'created_at': api_key.created_at,
                    'updated_at': api_key.updated_at,
                }, status=status.HTTP_200_OK)
            except CryptoExchangeAPI.DoesNotExist:
                return Response({'error': 'API key not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            api_keys = CryptoExchangeAPI.objects.filter(user=request.user)
            return Response([{
                'exchange': api_key.exchange,
                'is_active': api_key.is_active,
                'created_at': api_key.created_at,
                'updated_at': api_key.updated_at,
            } for api_key in api_keys], status=status.HTTP_200_OK)
    
    def post(self, request):
        """Handle POST requests for creating API keys.
        
        Args:
            request (Request): The HTTP request object.
            
        Returns:
            Response: A REST framework Response object containing the created API key.
        """
        exchange = request.data.get('exchange')
        api_key = request.data.get('api_key')
        api_secret = request.data.get('api_secret')
        
        if not all([exchange, api_key, api_secret]):
            return Response(
                {'error': 'Missing required parameters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if API key already exists for this exchange
        try:
            existing_key = CryptoExchangeAPI.objects.get(user=request.user, exchange=exchange)
            existing_key.api_key = api_key
            existing_key.api_secret = api_secret
            existing_key.is_active = True
            existing_key.save()
            return Response({
                'exchange': existing_key.exchange,
                'is_active': existing_key.is_active,
                'created_at': existing_key.created_at,
                'updated_at': existing_key.updated_at,
            }, status=status.HTTP_200_OK)
        except CryptoExchangeAPI.DoesNotExist:
            # Create new API key
            new_key = CryptoExchangeAPI.objects.create(
                user=request.user,
                exchange=exchange,
                api_key=api_key,
                api_secret=api_secret,
                is_active=True
            )
            return Response({
                'exchange': new_key.exchange,
                'is_active': new_key.is_active,
                'created_at': new_key.created_at,
                'updated_at': new_key.updated_at,
            }, status=status.HTTP_201_CREATED)
    
    def delete(self, request, exchange):
        """Handle DELETE requests for deleting API keys.
        
        Args:
            request (Request): The HTTP request object.
            exchange (str): The exchange to delete API keys for.
            
        Returns:
            Response: A REST framework Response object.
        """
        api_key = get_object_or_404(CryptoExchangeAPI, user=request.user, exchange=exchange)
        api_key.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)