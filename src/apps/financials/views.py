from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import services
from . import serializers

class FinancialsAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_financials(ticker)
        serializer = serializers.FinancialsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuarterlyFinancialsAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_quarterly_financials(ticker)
        serializer = serializers.FinancialsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)

class BalanceSheetAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_balance_sheet(ticker)
        serializer = serializers.FinancialsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuarterlyBalanceSheetAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_quarterly_balance_sheet(ticker)
        serializer = serializers.FinancialsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)

class CashflowAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_cashflow(ticker)
        serializer = serializers.FinancialsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuarterlyCashflowAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_quarterly_cashflow(ticker)
        serializer = serializers.FinancialsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)

class EarningsAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_earnings(ticker)
        serializer = serializers.FinancialsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuarterlyEarningsAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_quarterly_earnings(ticker)
        serializer = serializers.FinancialsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)
