from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class Garage(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    services = models.TextField(help_text="List the services offered, separated by commas")
    owner_name = models.CharField(max_length=200)
    contact = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    
    # Store images inside the static folder
    image = models.ImageField(upload_to='garage_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    pass
