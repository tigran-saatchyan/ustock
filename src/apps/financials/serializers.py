from rest_framework import serializers

class FinancialsSerializer(serializers.Serializer):
    """Serializer for financial data responses.

    This serializer is used for endpoints returning financial information.
    It contains a ticker symbol and a data field with financial details.

    Attributes:
        ticker (str): The ticker symbol.
        data (Any): A JSON field containing the financial data.
    """
    ticker = serializers.CharField(required=False)
    data = serializers.JSONField(required=False)
