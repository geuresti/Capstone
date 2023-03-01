from django.db import models
from django.contrib.auth.models import User
"""
from mongoengine import * # Document, fields

class Account(Document):
    user_id = IntField()
    pixel_map_ids = ListField(IntField())
    placeholder_image_ids = ListField(IntField())
"""
"""
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    pixel_map_ids = models.CharField(max_length=100)
    placeholder_image_ids = models.CharField(max_length=100)

    def __str__(self):
        return self.user.first_name
"""
#from django_mongoengine import Document, EmbeddedDocument, fields
#from mongoengine import *

class Account(models.Model): #EmbeddedDocument):
    placeholder = 0
#    user_id = fields.IntField()
#    pixel_map_ids = fields.ListField(fields.IntField())
#    placeholder_image_ids = fields.ListField(fields.IntField())
