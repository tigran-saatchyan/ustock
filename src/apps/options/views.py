from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import services
from . import serializers

class OptionsDatesAPIView(APIView):
    def get(self, request, ticker):
        data = services.get_options_dates(ticker)
        serializer = serializers.OptionsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)

class OptionsChainAPIView(APIView):
    def get(self, request, ticker):
        date = request.query_params.get('date')
        if not date:
            return Response({'error': 'Query parameter "date" is required'}, status=status.HTTP_400_BAD_REQUEST)
        data = services.get_option_chain(ticker, date)
        serializer = serializers.OptionsSerializer({'ticker': ticker, 'data': data})
        return Response(serializer.data, status=status.HTTP_200_OK)
