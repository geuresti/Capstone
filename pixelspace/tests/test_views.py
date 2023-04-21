from django.test import TestCase
from pixelspace import authentication as auth
from PIL import Image
from pixelspace.views import URLConverter
from pixelspace.forms import SaveForm, MapForm
import bcrypt
import pymongo
from pixelspace.models import GalleryDAO, PixelMapDAO

connect_string = 'mongodb+srv://mongodb_dao:uC3wPbLm7AIhkOUL@cluster0.nem4zbs.mongodb.net/?retryWrites=true&w=majority'
my_client = pymongo.MongoClient(connect_string)
dbname = my_client['pixelspace']

# CREATE A NEW COLLECTION FOR TESTING
test_users_collection = dbname["test_users"]
test_gallery_collection = dbname["test_gallery"]
test_pixelmaps_collection = dbname["test_pixelmaps"]

mongo_auth = auth.MongoAuthBackend()
gallery_dao = GalleryDAO()
pixelmap_dao = PixelMapDAO()

# once the views are separated into files, each
# view should probably get its own test class

class ViewTests(TestCase):

    def setUp(self):
        # set up user document to use in all tests
        encoded_password = "password".encode('utf-8')
        encrypted_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt(10))

        user = {
            "user_id": "999",
            "username" : "Lod",
            "password" : encrypted_password,
            "email" : "lod@gmail.com",
        }

        # Insert the document into the test database
        test_users_collection.insert_one(user)

        self.gallery_id = gallery_dao.create_gallery()

        self.pixel_map_id = pixelmap_dao.create_pixel_map(False, "dummy", "just for testing", 100, 150, True, False)

    def tearDown(self):
        #try:
        #    newest_map = dbname["pixelmaps"].find_one(
        #        sort=[( '_id', pymongo.DESCENDING )]
        #    )

        #    mapID = newest_map['pixelmap_id']
        #except:
        #    pass

        test_pixelmaps_collection.delete_many({})

        test_gallery_collection.delete_many({})

    def test_index_view(self):
        response = self.client.get('/pixelspace/')
        self.assertEqual(response.status_code, 200)

    def test_colors_view(self):
        response = self.client.get('/pixelspace/colors')
        self.assertEqual(response.status_code, 200)

    def test_colors_view_with_input_one(self):
        response = self.client.post('/pixelspace/colors', {"lightness":50, "axisA":50, "axisB":50})
        self.assertEqual(response.status_code, 200)

    def test_colors_view_with_input_two(self):
        response = self.client.post('/pixelspace/colors', {"lightness":50, "axisA":"", "axisB":50})
        self.assertEqual(response.status_code, 200)

    def test_colors_view_with_input_three(self):
        response = self.client.post('/pixelspace/colors', {"lightness":50, "axisA":50, "axisB":""})
        self.assertEqual(response.status_code, 200)

    def test_colors_view_with_input_four(self):
        response = self.client.post('/pixelspace/colors', {"lightness":"", "axisA":50, "axisB":50})
        self.assertEqual(response.status_code, 200)

    def test_colors_view_with_input_five(self):
        response = self.client.post('/pixelspace/colors', {"lightness":"", "axisA":"", "axisB":""})
        self.assertEqual(response.status_code, 200)

    def test_colors_view_with_input_six(self):
        response = self.client.post('/pixelspace/colors', {"lightness":999, "axisA":50, "axisB":50})
        self.assertEqual(response.status_code, 200)

    def test_colors_view_with_input_seven(self):
        response = self.client.post('/pixelspace/colors', {"lightness":0, "axisA":0, "axisB":0})
        self.assertEqual(response.status_code, 200)

    def test_colors_view_with_input_eight(self):
        response = self.client.post('/pixelspace/colors', {"lightness":1, "axisA":2, "axisB":3})
        self.assertEqual(response.status_code, 200)

    def test_gallery_view(self):
        response = self.client.get('/pixelspace/gallery')
        self.assertEqual(response.status_code, 200)

    def test_logo_view(self):
        response = self.client.get('/pixelspace/logo')
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get('/pixelspace/login')
        self.assertEqual(response.status_code, 200)

    # logs in user from main db
    def test_login_view_with_credentials(self):
        response = self.client.post('/pixelspace/login', {'username': 'Tak', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)

    def test_login_view_with_bad_credentials(self):
        response = self.client.post('/pixelspace/login', {'username': 'Tak', 'password': 'asodkoakds'})
        self.assertEqual(response.status_code, 400)

    def test_pixel_map_view(self):
        response = self.client.get('/pixelspace/pixelmap')
        self.assertEqual(response.status_code, 200)

    def test_settings_view(self):
        response = self.client.get('/pixelspace/settings')
        self.assertEqual(response.status_code, 200)

    def test_settings_view(self):
        # redirects because no one is logged in
        response = self.client.post('/pixelspace/settings', {"newPassword":"password", "retypePassword":"password", "deleteAccount":False})
        self.assertEqual(response.status_code, 302)

    def test_create_account_view(self):
        response = self.client.get('/pixelspace/create-account')
        self.assertEqual(response.status_code, 200)

    def test_create_account_view_new_user(self):
        mongo_auth.create_account("Jeff", "password", "jeff@gmail.com")
        user = mongo_auth.authenticate("test_users", username="Jeff", password="password")

        self.assertIsNotNone(user)

    def test_create_account_view_new_user(self):
        response = self.client.post('/pixelspace/create-account', {
            "username":"Jeff",
            "password":"ghj",
            "confirm_password":"asd",
            "email":"jeff@gmail.com"
        })

        self.assertEqual(response.status_code, 302)

    def test_create_account_valid_arguments(self):
        response = self.client.post('/pixelspace/create-account', {
            "username":"ckoisjpowkfekpor",
            "password":"mkmk",
            "confirm_password":"mkmk",
            "email":"ckoisjpowkfekpor@gmail.com"
        })

        mongo_auth.delete_user("ckoisjpowkfekpor", "users")

        self.assertEqual(response.status_code, 302)

    def test_create_account_invalid_arguments(self):
        response = self.client.post('/pixelspace/create-account', {
            "username":"ckoisjpowkfekpor",
            "password":"asdasd",
            "confirm_password":"mkmk",
            "email":"ckoisjpowkfekpor@gmail.com"
        })

        #mongo_auth.delete_user("ckoisjpowkfekpor", "users")

        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        response = self.client.get('/pixelspace/logout')
        # no account is logged in; redirect to index page
        self.assertEqual(response.status_code, 302)

    def test_results_view(self):
        response = self.client.get('/pixelspace/results')
        self.assertEqual(response.status_code, 200)

    #def test_results_view_submit_map(self):
    #    response = self.client.post('/pixelspace/results', {'png': ['on'], 'jpg': ['on'], 'tif': ['on']})
    #    self.assertEqual(response.status_code, 200)

    def test_results_view_delete_map(self):
        response = self.client.post('/pixelspace/results', {'deleteMap': ['on']})
        self.assertEqual(response.status_code, 302)

    def test_results_view_save_map(self):
        response = self.client.post('/pixelspace/results', {'submitMap': ['off']})
        self.assertEqual(response.status_code, 302)
