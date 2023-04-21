from django.test import TestCase
from pixelspace import authentication as auth
from pixelspace.models import GalleryDAO, PixelMapDAO
import bcrypt
import pymongo

connect_string = 'mongodb+srv://mongodb_dao:uC3wPbLm7AIhkOUL@cluster0.nem4zbs.mongodb.net/?retryWrites=true&w=majority'
my_client = pymongo.MongoClient(connect_string)
dbname = my_client['pixelspace']

# using a specific collection for testing
collection_name = "test_users"
collection = dbname[collection_name]

test_gallery_collection = dbname["test_gallery"]
test_pixelmaps_collection = dbname["test_pixelmaps"]

mongo_auth = auth.MongoAuthBackend()
gallery_dao = GalleryDAO()
pixelmap_dao = PixelMapDAO()

class UserModelTest(TestCase):

    def setUp(self):
        encoded_password = "password".encode('utf-8')
        encrypted_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt(10))

        # Set up user document to use in all tests
        user = {
            "user_id": "999",
            "username" : "Lod",
            "password" : encrypted_password,
            "email" : "lod@gmail.com",
        }

        # Insert the document into the test database
        collection.insert_one(user)

    def tearDown(self):
        # Delete dummy test account once tests are done
        delete_data = collection.delete_one({'user_id':'999'})

    def test_user_model(self):
        user = collection.find_one({"username": "Lod"})
        self.assertEqual(user['username'], 'Lod')

    def test_user_already_exists(self):
        username = "Lod"

        encoded_password = "password".encode('utf-8')
        encrypted_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt(10))

        user = {
            "user_id": "55",
            "username" : username,
            "password" : encrypted_password,
            "email" : "lod123@gmail.com",
        }

        # Insert the document into the test database
        already_exists = auth.MongoAuthBackend.already_exists(collection_name, username)

        self.assertTrue(already_exists)

    def test_get_user(self):
        mongo_auth.create_account("Jan", "password", "jan@gmail.com", collection_name="test_users")

        retrieve_user = mongo_auth.get_user("test_users", user_id=1)
        #print("RETRIEVE USER:", retrieve_user)
        self.assertIsNone(retrieve_user)

    def test_user_authenticate_valid_credentials(self):
        username = "Lod"
        password = "password"

        user = mongo_auth.authenticate(collection_name, username, password)
        self.assertTrue(user)

    def test_user_authenticate_invalid_password(self):
        username = "Lod"
        password = "wrong_password"

        user = mongo_auth.authenticate(collection_name, username, password)
        self.assertFalse(user)

    def test_user_authenticate_invalid_username(self):
        username = "Dol"
        password = "password"

        user = mongo_auth.authenticate(collection_name, username, password)
        self.assertFalse(user)

class PixelMapModelTest(TestCase):
    def setUp(self):
        self.pixel_map_id = pixelmap_dao.create_pixel_map(False, "dummy", "just for testing", 100, 150, True, False)

    def tearDown(self):
        test_pixelmaps_collection.delete_many({})

    def test_create_pixel_map_no_color_specified(self):
        map_id = pixelmap_dao.create_pixel_map(False, "some_user", "running a test", 150, 175, False, False)
        self.assertIsNotNone(map_id)

    def test_create_pixel_map_greyscale(self):
        map_id = pixelmap_dao.create_pixel_map(False, "some_user", "running a test", 150, 175, True, False)
        self.assertIsNotNone(map_id)

    def test_create_pixel_map_color_range_blank(self):
        map_id = pixelmap_dao.create_pixel_map(False, "some_user", "running a test", 150, 175, False, True)
        self.assertIsNotNone(map_id)

    def test_create_pixel_map_color_range_specified(self):
        map_id = pixelmap_dao.create_pixel_map(False, "some_user", "running a test", 150, 175, False, True, [0, 50], [50, 100], [100, 150])
        self.assertIsNotNone(map_id)

class GalleryModelTest(TestCase):

    def setUp(self):
        self.gallery_id = gallery_dao.create_gallery()

    def tearDown(self):
        test_gallery_collection.delete_many({})

    def test_empty_gallery(self):
        self.assertEqual(gallery_dao.empty_gallery(0), 1)

    def test_add_pixel_map(self):
        self.assertEqual(gallery_dao.add_pixel_map(0, 5), 1)
