from rest_framework import serializers

class StrategySerializer(serializers.Serializer):
    strategy_id = serializers.CharField()
    index = serializers.CharField()
    strike_price = serializers.IntegerField()
    expiry = serializers.CharField()
    option = serializers.CharField()
    chart_time = serializers.CharField()