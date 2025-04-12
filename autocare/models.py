from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class GarageLocation(models.Model):
    address = models.CharField(max_length=255)  # e.g., "Ngong Road, Nairobi"
    latitude = models.DecimalField(max_digits=9, decimal_places=6)   # e.g., -1.292066
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # e.g., 36.821945

    def __str__(self):
        return self.address
    
    
class GarageService(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    


class Garage(models.Model):
    name = models.CharField(max_length=200)
    location = models.ForeignKey(GarageLocation, on_delete=models.CASCADE)
    services = models.ManyToManyField(GarageService)
    owner_name = models.CharField(max_length=200)
    contact = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='garage_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    
class User(AbstractUser):
    pass
