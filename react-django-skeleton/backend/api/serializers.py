from rest_framework import serializers
from .models import User, AirQuality


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "is_admin")

class AirQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AirQuality
        fields = '__all__'
