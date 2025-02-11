from rest_framework import serializers

class TickerDataSerializer(serializers.Serializer):
    ticker = serializers.CharField(required=False)
    data = serializers.JSONField(required=False)
