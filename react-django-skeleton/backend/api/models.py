from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200, default="")
    is_admin = models.BooleanField(null=False, default=False)

class AirQuality(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    pm1_0_concentration = models.DecimalField(max_digits=5, decimal_places=2)
    pm2_5_concentration = models.DecimalField(max_digits=5, decimal_places=2)
    pm10_concentration = models.DecimalField(max_digits=5, decimal_places=2)
