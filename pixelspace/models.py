from django.db import models
import pymongo
from PIL import Image
import random

connect_string = 'mongodb+srv://mongodb_dao:uC3wPbLm7AIhkOUL@cluster0.nem4zbs.mongodb.net/?retryWrites=true&w=majority'
my_client = pymongo.MongoClient(connect_string)
dbname = my_client['pixelspace']

# collection_name = "test_pixelmaps"
# collection = dbname[collection_name]

class User():
    user_id = None
    username = None
    password = None
    email = None
    pixel_map_ids = []
    placeholder_image_ids = []

    def __str__(self):
        return self.username

class PixelMapDAO:

    def __init__(self, collection_name="test_pixelmaps"):
        self.collection_name = collection_name
        self.collection = dbname[collection_name]

    def create_pixel_map(self, show_image, username, caption, length, width, greyscale, custom, red_range=[0,255], green_range=[0,255], blue_range=[0,255]):

        #generate placeholder image in which to fill in with pixels
        img = Image.new('RGB', [length, width], 'pink')

        #the process is similar for if the maps are greyscale or color
        #generate a random value between 1-255, and apply to rgb balues
        #append onto a list of values, which then gets mapped to the image
        if custom == True:
            colorRange = [
                red_range[0],
                blue_range[0],
                green_range[0],
                red_range[1],
                blue_range[1],
                green_range[1]
            ]

            for item in range(len(colorRange)):

                if colorRange[item] == None and item < 3:
                    print(colorRange[item])
                    colorRange[item] = 1

                if colorRange[item] == None and item >= 3:
                    print(colorRange[item])
                    colorRange[item] = 255

            listCustom= [0] * (width * length )
            for x in range(width * length ):
                r = random.randint(colorRange[0], colorRange[3])
                g = random.randint(colorRange[2], colorRange[5])
                b = random.randint(colorRange[1], colorRange[4])
                listCustom[x] = (r, g, b)

            img.putdata(listCustom)
            #img.show()

        elif greyscale == True:
            listGrey= [0] * (width * length)

            for x in range(width * length):
                Grey = random.randint(1,255)
                listGrey[x] = (Grey,Grey,Grey)

            img.putdata(listGrey)
            #img.show()

        else:
            listColor = [0] * (width * length)
            for x in range(width * length):
                r = random.randint(1, 255)
                g = random.randint(1, 255)
                b = random.randint(1, 255)
                listColor[x] = (r,g,b)

            img.putdata(listColor)
            #img.show()

        if show_image:
            img.show()

        #get the previous map
        try:
            most_recent_map = self.collection.find_one(
                sort=[( '_id', pymongo.DESCENDING )]
            )

            #increment the id of the previous map to get the id for the current map
            map_id = int(most_recent_map["pixelmap_id"]) + 1
        except:
            map_id = 0

        #convert image to binary in order to store in the database
        bin = img.tobytes()

        #insert pixelmap into database
        pixelmap = {
            "pixelmap_id": map_id,
            "creator" : username,
            "caption" : caption,
            "PixelMap" : bin,
            "width" : width,
            "length" : length,
            "likes" : 0,
            }

        self.collection.insert_one(pixelmap)
        return map_id

#    def delete_pixel_map(self, ):
#        return -1

#    def get_pixel_map(self, ):
#        return -1

#    def get_all_pixel_maps(self, ):
#        return -1

#    def add_pixel_map_to_database(self, ):
#        return -1

class GalleryDAO:

    def __init__(self, collection_name="test_gallery"):
        self.collection_name = collection_name
        self.collection = dbname[collection_name]

    def create_gallery(self):
        gallery = self.collection.find_one(
            sort=[( '_id', pymongo.DESCENDING )]
        )

        try:
            gallery_id = int(gallery["gallery_id"]) + 1
        except:
            # if the database has no galleries in it yet
            gallery_id = 0

        new_gallery = {
            "gallery_id": gallery_id,
            "gallery_images" : [],
        }

        self.collection.insert_one(new_gallery)
        #print("New Gallery Successfully Created")

        return gallery_id

    def remove_pixel_map(self):
        return -1

    def empty_gallery(self, gallery_id):
        try:
            gallery = self.collection.find_one(
                {'gallery_id': gallery_id}
            )

            self.collection.update_one({'gallery_id': gallery_id}, {'$set':{'gallery_images':[]}})
            return 1

        except:
            return -1

    def add_pixel_map(self, galleryID, mapID):
        self.collection.update_one({'gallery':galleryID}, {'$push':{'gallery_images':mapID}})
        return 1
