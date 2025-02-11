from rest_framework import serializers

class TickerDataSerializer(serializers.Serializer):
    """Serializer for ticker data responses.

    This serializer is used for endpoints that return information related to a specific ticker.
    It contains two fields:
      - ticker: A string representing the ticker symbol.
      - data: A JSON field containing the associated data (e.g., financial metrics, historical prices, etc.).

    Attributes:
        ticker (str): The ticker symbol.
        data (Any): A JSON object with data related to the ticker.
    """
    ticker = serializers.CharField(required=False)
    data = serializers.JSONField(required=False)
