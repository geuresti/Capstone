from django.db import models

# This file should manage account creation
# there are some fields we didn't include in the initial kickoff
# of the user database (pixel_map_ids, placeholder_image_ids, email)
# The User model should have a create() function, login(), logout()
# as well as functionality to check for valid passwords

# what does extending models.Model do?
class User(): #models.Model):
    user_id = None
    username = None
    password = None
    email = None
    pixel_map_ids = []
    placeholder_image_ids = []

    def create_user(username, password, confirm_password, email):
        return 0

    def authenticate_user(username, password):
        return 0

#    def logout_user(username, password):

    def __str__(self):
        return self.username
