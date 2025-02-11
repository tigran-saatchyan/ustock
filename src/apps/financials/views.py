from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import services
from . import serializers


class FinancialsAPIView(APIView):
    """API view for retrieving annual financial data for a given ticker.

    This endpoint fetches the annual financial data using the
    `services.get_financials` function and serializes the result with the
    `FinancialsSerializer`.

    Attributes:
        None.
    """

    def get(self, request, ticker):
        """Handle GET requests for annual financial data.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which the financial data is requested.

        Returns:
            Response: A REST framework Response object containing the serialized
            financial data with an HTTP 200 OK status.
        """
        data = services.get_financials(ticker)
        serializer = serializers.FinancialsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuarterlyFinancialsAPIView(APIView):
    """API view for retrieving quarterly financial data for a given ticker.

    This endpoint obtains the quarterly financial data via
    `services.get_quarterly_financials` and returns the data serialized with
    `FinancialsSerializer`.

    Attributes:
        None.
    """

    def get(self, request, ticker):
        """Handle GET requests for quarterly financial data.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which the quarterly financial data is requested.

        Returns:
            Response: A REST framework Response object containing the serialized
            quarterly financial data with an HTTP 200 OK status.
        """
        data = services.get_quarterly_financials(ticker)
        serializer = serializers.FinancialsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BalanceSheetAPIView(APIView):
    """API view for retrieving the annual balance sheet for a given ticker.

    This endpoint retrieves the balance sheet data by calling
    `services.get_balance_sheet` and serializes it using `FinancialsSerializer`.

    Attributes:
        None.
    """

    def get(self, request, ticker):
        """Handle GET requests for the balance sheet data.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which the balance sheet is requested.

        Returns:
            Response: A REST framework Response object containing the serialized
            balance sheet data with an HTTP 200 OK status.
        """
        data = services.get_balance_sheet(ticker)
        serializer = serializers.FinancialsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuarterlyBalanceSheetAPIView(APIView):
    """API view for retrieving the quarterly balance sheet for a given ticker.

    This endpoint uses `services.get_quarterly_balance_sheet` to fetch the data
    and serializes the result with `FinancialsSerializer`.

    Attributes:
        None.
    """

    def get(self, request, ticker):
        """Handle GET requests for the quarterly balance sheet data.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which the quarterly balance sheet is requested.

        Returns:
            Response: A REST framework Response object containing the serialized
            quarterly balance sheet data with an HTTP 200 OK status.
        """
        data = services.get_quarterly_balance_sheet(ticker)
        serializer = serializers.FinancialsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CashflowAPIView(APIView):
    """API view for retrieving the annual cashflow statement for a given ticker.

    This endpoint obtains the cashflow data via `services.get_cashflow` and
    returns the result serialized with `FinancialsSerializer`.

    Attributes:
        None.
    """

    def get(self, request, ticker):
        """Handle GET requests for the cashflow statement.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which the cashflow data is requested.

        Returns:
            Response: A REST framework Response object containing the serialized
            cashflow data with an HTTP 200 OK status.
        """
        data = services.get_cashflow(ticker)
        serializer = serializers.FinancialsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuarterlyCashflowAPIView(APIView):
    """API view for retrieving the quarterly cashflow statement for a given ticker.

    This endpoint retrieves quarterly cashflow data using
    `services.get_quarterly_cashflow` and serializes it with `FinancialsSerializer`.

    Attributes:
        None.
    """

    def get(self, request, ticker):
        """Handle GET requests for the quarterly cashflow statement.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which the quarterly cashflow data is requested.

        Returns:
            Response: A REST framework Response object containing the serialized
            quarterly cashflow data with an HTTP 200 OK status.
        """
        data = services.get_quarterly_cashflow(ticker)
        serializer = serializers.FinancialsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)


class EarningsAPIView(APIView):
    """API view for retrieving the annual earnings (income statement) for a given ticker.

    This endpoint calls `services.get_earnings` to fetch the annual income statement
    data (using Ticker.income_stmt) and serializes the result with `FinancialsSerializer`.

    Attributes:
        None.
    """

    def get(self, request, ticker):
        """Handle GET requests for annual earnings data.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which the earnings data is requested.

        Returns:
            Response: A REST framework Response object containing the serialized
            earnings data with an HTTP 200 OK status.
        """
        data = services.get_earnings(ticker)
        serializer = serializers.FinancialsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuarterlyEarningsAPIView(APIView):
    """API view for retrieving the quarterly earnings (income statement) for a given ticker.

    This endpoint retrieves quarterly earnings data via
    `services.get_quarterly_earnings` (using Ticker.quarterly_income_stmt) and serializes
    the result with `FinancialsSerializer`.

    Attributes:
        None.
    """

    def get(self, request, ticker):
        """Handle GET requests for quarterly earnings data.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which the quarterly earnings data is requested.

        Returns:
            Response: A REST framework Response object containing the serialized
            quarterly earnings data with an HTTP 200 OK status.
        """
        data = services.get_quarterly_earnings(ticker)
        serializer = serializers.FinancialsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)
