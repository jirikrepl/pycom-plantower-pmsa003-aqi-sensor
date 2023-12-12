from django.contrib import admin
from django.urls import include, path
from .views import UserView, ReactView, AQIView

urlpatterns = [
    path("", ReactView.as_view()),
    path("aqi", AQIView.as_view())
]
