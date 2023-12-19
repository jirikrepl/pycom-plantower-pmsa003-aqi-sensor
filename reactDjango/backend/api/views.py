from rest_framework import generics
from .models import User, AirQuality
from .serializers import UserSerializer, AirQualitySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from django.db.models.functions import Trunc

# Create your views here.
class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ReactView(APIView):
    def get(self, request):
        # output = [{"name": "John", "age": 27}, {"name": "Mary", "age": 25}]
        return Response("THIS IS A TEST")

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

# Averages for PM1.0, PM2.5, and PM10 concentrations, grouped by each hour.
# Returns the results as a JSON response.
class AQIView(APIView):
    def get(self, request):
        hourly_averages = (
            AirQuality.objects
            .annotate(datetime=Trunc('timestamp', 'hour'))
            .values('datetime')
            .annotate(
                pm1_0_concentration=Avg('pm1_0_concentration'),
                pm2_5_concentration=Avg('pm2_5_concentration'),
                pm10_concentration=Avg('pm10_concentration')
            )
            .order_by('datetime')
        )
        hourly_averages_list = list(hourly_averages)
        return Response(hourly_averages_list)

    def post(self, request):
        serializer = AirQualitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
