from django.test import TestCase

from pixelspace import authentication as auth

import pymongo

connect_string = 'mongodb+srv://mongodb_dao:uC3wPbLm7AIhkOUL@cluster0.nem4zbs.mongodb.net/?retryWrites=true&w=majority'
my_client = pymongo.MongoClient(connect_string)
dbname = my_client['pixelspace']

# CREATE A NEW COLLECTION FOR TESTING
collection_name = "test_users"
collection = dbname[collection_name]

mongo_auth = auth.MongoAuthBackend()

class UserModelTest(TestCase):

    def setUp(self):
        # Set up user document to use in all tests
        user = {
            "user_id": "999",
            "username" : "Lod",
            "password" : "password",
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

        user = {
            "user_id": "55",
            "username" : username,
            "password" : "password",
            "email" : "lod123@gmail.com",
        }

        # Insert the document into the test database
        already_exists = auth.MongoAuthBackend.already_exists(collection_name, username)

        self.assertTrue(already_exists)

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
