from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    api_url = models.URLField(max_length=500)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    sensor_location = models.CharField(max_length=255, blank=True, null=True)
    sensor_name = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
