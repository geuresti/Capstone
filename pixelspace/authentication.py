from django.contrib.auth.backends import BaseBackend
import pymongo
import bcrypt

connect_string = 'mongodb+srv://mongodb_dao:uC3wPbLm7AIhkOUL@cluster0.nem4zbs.mongodb.net/?retryWrites=true&w=majority'
my_client = pymongo.MongoClient(connect_string)
dbname = my_client['pixelspace']

security_questions = {
    'Q1':'What is the name of your first pet?',
    'Q2':'What is your favorite ice cream flavor?',
    'Q3':'What was your favorite stuffed animal?',
    'Q4':'What is your favorite sports team?',
    'Q5':'What is the name of your high school?',
    'Q6':'What is the name of your favorite teacher?'
}

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
            encoded_password = password.encode('utf-8')

            if bcrypt.checkpw(encoded_password, user['password']):
                    return user
        return None

    def login(self, request, user):
        request.session['username'] = user['username']

    def change_password(self, collection_name="users", username=None, new_password=None):
        if username and new_password:
            collection = dbname[collection_name]
            user = collection.find_one({"username": username})

            if user:
                encrypted_password = new_password.encode('utf-8')
                hashed_password = bcrypt.hashpw(encrypted_password, bcrypt.gensalt(10))

                collection.update_one({'username':username}, {'$set':{'password':hashed_password}})

    def delete_user(self, username, collection_name="test_users"):
        collection = dbname[collection_name]
        collection.delete_one({'username':username})
        print("Successfully deleted user:", username)

    def create_account(self, username, password, email, security_q1, answer1, security_q2, answer2, collection_name="test_users"):
        collection = dbname[collection_name]
        newest_user = collection.find_one(
            sort=[( '_id', pymongo.DESCENDING )]
        )

        try:
            new_user_id = int(newest_user["user_id"]) + 1
        except:
            # if the database has no user in it yet
            new_user_id = 0

        encoded_password = password.encode('utf-8')
        encrypted_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt(10))

        sec_question_one = security_questions[security_q1]
        sec_question_two = security_questions[security_q2]

        new_user = {
            "user_id": new_user_id,
            "username" : username,
            "password" : encrypted_password,
            "pixelmap_ids": [],
            "sec_q1": sec_question_one,
            "sec_q2": sec_question_two,
            "sec_a1": answer1,
            "sec_a2": answer2,
            "email" : email,
        }

        collection.insert_one(new_user)
        print("Account successfully created")

    @classmethod
    def already_exists(self, collection_name="test_users", username=None):
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
