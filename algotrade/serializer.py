from rest_framework import serializers

class StrategySerializer(serializers.Serializer):
    strategy_id = serializers.CharField(max_length=50)
    index = serializers.CharField(max_length=50)
    strike_price = serializers.IntegerField(max_length=50)
    expiry = serializers.CharField(max_length=50)
    option = serializers.CharField(max_length=50)
    chart_time = serializers.CharField(max_length=50)