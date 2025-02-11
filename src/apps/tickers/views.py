from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import services
from . import serializers


class TickerInfoAPIView(APIView):
    """API view to retrieve ticker information.

    This endpoint returns detailed information about a given ticker
    by fetching data from the yFinance service.
    """

    def get(self, request, ticker):
        """Handle GET requests to retrieve ticker information.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which the information is requested.

        Returns:
            Response: A REST framework Response containing the serialized ticker information with a 200 status.
        """
        data = services.get_ticker_info(ticker)
        serializer = serializers.TickerDataSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TickerHistoryAPIView(APIView):
    """API view to retrieve historical price data for a ticker.

    This endpoint returns historical data (price history) for a given ticker
    over a specified date range and interval.
    """

    def get(self, request, ticker):
        """Handle GET requests to retrieve ticker historical data.

        Query Parameters:
            start (str): Start date in YYYY-MM-DD format.
            end (str): End date in YYYY-MM-DD format.
            interval (str, optional): Data interval (default is '1d').

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which historical data is requested.

        Returns:
            Response: A REST framework Response containing the serialized historical data with a 200 status.
        """
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        interval = request.query_params.get('interval', '1d')
        data = services.get_ticker_history(ticker, start, end, interval)
        serializer = serializers.TickerDataSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TickerDividendsAPIView(APIView):
    """API view to retrieve dividend data for a ticker.

    This endpoint returns dividend information for a given ticker.
    """

    def get(self, request, ticker):
        """Handle GET requests to retrieve ticker dividend data.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which dividend data is requested.

        Returns:
            Response: A REST framework Response containing the serialized dividend data with a 200 status.
        """
        data = services.get_ticker_dividends(ticker)
        serializer = serializers.TickerDataSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TickerSplitsAPIView(APIView):
    """API view to retrieve stock splits data for a ticker.

    This endpoint returns stock splits information for a given ticker.
    """

    def get(self, request, ticker):
        """Handle GET requests to retrieve ticker splits data.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which splits data is requested.

        Returns:
            Response: A REST framework Response containing the serialized splits data with a 200 status.
        """
        data = services.get_ticker_splits(ticker)
        serializer = serializers.TickerDataSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TickerRecommendationsAPIView(APIView):
    """API view to retrieve analyst recommendations for a ticker.

    This endpoint returns recommendation data for a given ticker.
    """

    def get(self, request, ticker):
        """Handle GET requests to retrieve ticker recommendations.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which recommendation data is requested.

        Returns:
            Response: A REST framework Response containing the serialized recommendation data with a 200 status.
        """
        data = services.get_ticker_recommendations(ticker)
        serializer = serializers.TickerDataSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TickerCalendarAPIView(APIView):
    """API view to retrieve event calendar data for a ticker.

    This endpoint returns upcoming events (earnings, announcements, etc.) for a given ticker.
    """

    def get(self, request, ticker):
        """Handle GET requests to retrieve the event calendar for the ticker.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which event calendar data is requested.

        Returns:
            Response: A REST framework Response containing the serialized calendar data with a 200 status.
        """
        data = services.get_ticker_calendar(ticker)
        serializer = serializers.TickerDataSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TickerSustainabilityAPIView(APIView):
    """API view to retrieve sustainability (ESG) data for a ticker.

    This endpoint returns ESG and sustainability information for a given ticker.
    """

    def get(self, request, ticker):
        """Handle GET requests to retrieve ticker sustainability data.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which sustainability data is requested.

        Returns:
            Response: A REST framework Response containing the serialized sustainability data with a 200 status.
        """
        data = services.get_ticker_sustainability(ticker)
        serializer = serializers.TickerDataSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TickerHoldersAPIView(APIView):
    """API view to retrieve information on institutional and major holders for a ticker.

    This endpoint returns data about the holders of a given ticker.
    """

    def get(self, request, ticker):
        """Handle GET requests to retrieve ticker holders data.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which holder data is requested.

        Returns:
            Response: A REST framework Response containing the serialized holders data with a 200 status.
        """
        data = services.get_ticker_holders(ticker)
        serializer = serializers.TickerDataSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TickerNewsAPIView(APIView):
    """API view to retrieve news related to a ticker.

    This endpoint returns news articles and related information for a given ticker.
    """

    def get(self, request, ticker):
        """Handle GET requests to retrieve ticker news.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which news is requested.

        Returns:
            Response: A REST framework Response containing the serialized news data with a 200 status.
        """
        data = services.get_ticker_news(ticker)
        serializer = serializers.TickerDataSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)
