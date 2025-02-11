from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import services
from . import serializers

class TickerInfoAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_ticker_info(ticker)
        serializer = serializers.TickerDataSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TickerHistoryAPIView(APIView):
    def get(self, request, ticker):
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        interval = request.query_params.get('interval', '1d')
        data = services.get_ticker_history(ticker, start, end, interval)
        serializer = serializers.TickerDataSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)

class TickerDividendsAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_ticker_dividends(ticker)
        serializer = serializers.TickerDataSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)

class TickerSplitsAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_ticker_splits(ticker)
        serializer = serializers.TickerDataSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)

class TickerRecommendationsAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_ticker_recommendations(ticker)
        serializer = serializers.TickerDataSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)

class TickerCalendarAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_ticker_calendar(ticker)
        serializer = serializers.TickerDataSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)

class TickerSustainabilityAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_ticker_sustainability(ticker)
        serializer = serializers.TickerDataSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)

class TickerHoldersAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_ticker_holders(ticker)
        serializer = serializers.TickerDataSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)

class TickerNewsAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_ticker_news(ticker)
        serializer = serializers.TickerDataSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)
