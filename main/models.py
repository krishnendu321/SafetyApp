from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15)
    aadhar = models.ImageField(upload_to='aadhar/')
    is_verified = models.BooleanField(default=False)  # Already exists
    is_active = models.BooleanField(default=True)     # Already exists

    def is_approved_user(self):
        return self.is_verified and self.is_active

class EmergencyContact(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class PoliceStation(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    map_link = models.URLField()

    def __str__(self):
        return self.name

class SOSRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def get_google_maps_link(self):
        if self.latitude and self.longitude:
            return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
        return None

    def __str__(self):
        return f"SOS from {self.user.username} at {self.timestamp}"
