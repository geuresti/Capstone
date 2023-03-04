import pymongo

# mongodb_dao / uC3wPbLm7AIhkOUL
connect_string = 'mongodb+srv://mongodb_dao:uC3wPbLm7AIhkOUL@cluster0.nem4zbs.mongodb.net/?retryWrites=true&w=majority'

my_client = pymongo.MongoClient(connect_string)

# First define the database name
dbname = my_client['pixelspace']

# Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection
collection_name = dbname["users"]

# Read the documents
user_details = collection_name.find({})

# Print out all user documents
gol = collection_name.find_one({"username": "Gol"})

#for user in user_details:
    #print(f'USER #{user["user_id"]}:', user["username"])
'''
# Create a user document
user = {
    "user_id": "99",
    "username" : "Zzz",
    "password" : "password",
    "email" : "Zzz@gmail.com",
}

# Insert the documents
#collection_name.insert_many([user_1, user_2])
collection_name.insert_one(user)

# Read the documents
user_details = collection_name.find({})

# Print out all user documents
for user in user_details:
    print(f'USER #{user["user_id"]}:', user["username"])

# Grab the most recently added user
latest_user = collection_name.find_one(
  sort=[( '_id', pymongo.DESCENDING )]
)
#print(latest_user)

# Check if user exists
does_user_exist = collection_name.find_one({"username": "Gol"})
print("TEST:", does_user_exist)
#print(does_user_exist['email'])

# Update one document
update_data = collection_name.update_one({'medicine_id':'RR000123456'}, {'$set':{'common_name':'Paracetamol 500'}})

# Delete one document
delete_data = collection_name.delete_one({'medicine_id':'RR000123456'})
'''
