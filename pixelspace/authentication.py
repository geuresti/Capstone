from django.contrib.auth.backends import BaseBackend
import pymongo

connect_string = 'mongodb+srv://mongodb_dao:uC3wPbLm7AIhkOUL@cluster0.nem4zbs.mongodb.net/?retryWrites=true&w=majority'
my_client = pymongo.MongoClient(connect_string)
dbname = my_client['pixelspace']
users_collection = dbname["users"]

# django.contrib.auth authenticate does not work because
# djang Users have an attribute ".backend" which keeps track
# of which backend authenticator successfully authenticated
# the credentials. MongoDB documents are DICTIONARIES and do
# not have the .backend attribute.
class MongoAuthBackend(BaseBackend):
    def authenticate(self, collection_name="users", username=None, password=None):
        collection = dbname[collection_name]
        user = collection.find_one({"username": username})
        if user:
            if user['password'] == password:
                return user
        return None

    def login(self, request, user):
        request.session['username'] = user['username']

    @classmethod
    def already_exists(self, collection_name="users", username=None):
        collection = dbname[collection_name]
        user = collection.find_one({"username": username})
        if user:
            return True

        return False

    def get_user(self, collection_name="users", user_id=None):
        try:
            return collection_name.find_one({"user_id": user_id})
        except:
            return None
