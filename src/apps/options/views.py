from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import services, serializers


class OptionsDatesAPIView(APIView):
    """API view to retrieve available options expiration dates for a given ticker.

    This view calls the corresponding service function to fetch the list of
    available options expiration dates and returns the result serialized
    with OptionsSerializer.
    """

    def get(self, request, ticker):
        """Handle GET requests to retrieve options expiration dates.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which options dates are requested.

        Returns:
            Response: A REST framework Response object containing the serialized
                options dates data with an HTTP 200 OK status.
        """
        data = services.get_options_dates(ticker)
        serializer = serializers.OptionsSerializer(
            {'ticker': ticker, 'data': data}
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class OptionsChainAPIView(APIView):
    """API view to retrieve the options chain for a given ticker and expiration date.

    This view fetches the options chain data for the specified ticker and date,
    serializes it using OptionsSerializer, and returns the result.
    """

    def get(self, request, ticker):
        """Handle GET requests to retrieve the options chain data.

        Args:
            request (Request): The HTTP request object.
            ticker (str): The ticker symbol for which the options chain is requested.

        Returns:
            Response: A REST framework Response object containing the serialized
                options chain data with an HTTP 200 OK status. If the "date" query
                parameter is missing, returns an error response with HTTP 400 Bad Request.
        """
        date = request.query_params.get('date')
        if not date:
            return Response(
                {'error': 'Query parameter "date" is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = services.get_option_chain(ticker, date)
        serializer = serializers.OptionsSerializer(
            {'ticker': ticker, 'data': data}
            )
        return Response(serializer.data, status=status.HTTP_200_OK)
