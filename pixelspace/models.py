from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    pixel_map_ids = models.CharField(max_length=100)
    placeholder_image_ids = models.CharField(max_length=100)

    def __str__(self):
        return self.user.first_name
