from django.db import models

class User():
    user_id = None
    username = None
    password = None
    email = None
    pixel_map_ids = []
    placeholder_image_ids = []

    def __str__(self):
        return self.username
