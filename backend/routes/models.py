from django.db import models


class CityProfile(models.Model):
    name = models.CharField(max_length=100, unique=True)
    region = models.CharField(max_length=80, default='region')
    avg_temperature_c = models.FloatField(default=21.0)
    avg_rain_mm = models.FloatField(default=3.0)
    avg_wind_kph = models.FloatField(default=12.0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TripRequest(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_date = models.DateField()
    preferred_temperature_c = models.FloatField(default=22.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.origin} -> {self.destination} on {self.departure_date}'
