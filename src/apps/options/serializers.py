from rest_framework import serializers

class OptionsSerializer(serializers.Serializer):
    """Serializer for options endpoints.

    This serializer is used to represent options data for a given ticker.

    Attributes:
        ticker (str): The ticker symbol.
        data (Any): A JSON field containing options-related data, such as available expiration dates or the option chain details.
    """
    ticker = serializers.CharField(required=False)
    data = serializers.JSONField(required=False)
