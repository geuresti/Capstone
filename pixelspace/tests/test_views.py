from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from pixelspace.models import Account

# once the views are separated into files, each
# view should probably get its own test class

"""
@classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass
"""

class ViewTests(TestCase):

    def test_index_view(self):
        print("Testing index view")
        response = self.client.get('/pixelspace/')
        self.assertEqual(response.status_code, 200)

    def test_colors_view(self):
        print("Testing colors view")
        response = self.client.get('/pixelspace/colors')
        self.assertEqual(response.status_code, 200)

    def test_image_view(self):
        print("Testing image view")
        response = self.client.get('/pixelspace/image')
        self.assertEqual(response.status_code, 200)

    def test_logo_view(self):
        print("Testing logo view")
        response = self.client.get('/pixelspace/logo')
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        print("Testing login view")
        response = self.client.get('/pixelspace/login')
        self.assertEqual(response.status_code, 200)

    def test_pixel_map_view(self):
        print("Testing pixelmap view")
        response = self.client.get('/pixelspace/pixelmap')
        self.assertEqual(response.status_code, 200)

    def test_settings_view(self):
        print("Testing settings view")
        response = self.client.get('/pixelspace/settings')
        self.assertEqual(response.status_code, 200)

    def test_create_account_view(self):
        print("Testing create account view")
        response = self.client.get('/pixelspace/create-account')
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        print("Testing logout view")
        response = self.client.get('/pixelspace/logout')
        # no account is logged in; redirect to index page
        self.assertEqual(response.status_code, 302)
