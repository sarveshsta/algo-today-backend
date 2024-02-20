from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    phone = serializers.IntegerField()
    otp = serializers.IntegerField()
    password = serializers.CharField(max_length=30)
    
class SignupSerializer(serializers.Serializer):
    phone = serializers.IntegerField()
    otp = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=30)
     
class SignupSerializer(serializers.Serializer):
    password = serializers.IntegerField()
    phone = serializers.IntegerField()
