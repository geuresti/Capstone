from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
import base64
from http import HTTPStatus
import os, sys
from .forms import AccountForm, UserForm, SettingsForm, LABForm, confirmDeleteForm, PixelForm, SaveForm, MapForm, confirmMapDeleteForm, CustomForm, LikeForm, commentForm, ShapeForm, RectangleForm, OvalForm, PolyForm
from django.contrib import messages
from colormath.color_objects import LabColor, sRGBColor, AdobeRGBColor
from colormath.color_objects import BT2020Color
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976
from coloraide.everything import ColorAll as Color
import pymongo
from PIL import Image,ImageDraw, ImageFont
import random
from bson.binary import Binary
import re
import bcrypt
from io import BytesIO

from .authentication import MongoAuthBackend

#   Connect to the mongodb database
connect_string = 'mongodb+srv://mongodb_dao:uC3wPbLm7AIhkOUL@cluster0.nem4zbs.mongodb.net/?retryWrites=true&w=majority'
my_client = pymongo.MongoClient(connect_string)

# database name
dbname = my_client['pixelspace']

# get collection name (create new collection if it doesn't exist)
users_collection = dbname["users"]
pixelmaps_collection = dbname["pixelmaps"]
gallery_collection = dbname["gallery"]
comments_collection = dbname["comment"]

mongo_auth = MongoAuthBackend()

def index(request):

    # There are some weird items in here
    # "_auth_user_id", "_auth_user_backend", "_auth_user_hash"
    # I THINK these are leftover values from the sqlite db
    # need to remove them and see if it causes any issues
#    del request.session['test']

    print("----------------\n", request.session)
    #request.session['test'] = 'testing'
    for data in request.session.keys():
        print(f'request.session[{data}]:', request.session[data])
    #print("\n", request.session['test'], "\n----------------")
    print("----------------")

    return render(request, 'pixelspace/index.html')

#View Function for the Colors template
def colors(request):
    template = loader.get_template('pixelspace/colors.html')
    if request.method == 'POST':
        #take in L*A*B values
        form = LABForm(request.POST)
        #if the inputs are valid
        if form.is_valid():
            lightness1 = form.cleaned_data.get("lightness")
            axisA = form.cleaned_data.get("axisA")
            axisB = form.cleaned_data.get("axisB")
            testing = [lightness1, axisA, axisB]
            print(testing)
            #format the Color to be a LAB
            colorRGB = Color("lab", testing)
            colorsRGB = Color("lab", testing)
            colorPro = Color("lab", testing)
            print(colorPro)
            #check if color is in gamut (an appropriate conversion)
            if colorRGB.in_gamut('a98-rgb'):
                rgbColor = colorRGB.convert("a98-rgb")
                print(rgbColor)
                rgbR = rgbColor['r'] * 255
                rgbG = rgbColor['g'] * 255
                rgbB = rgbColor['b'] * 255
                #Upscale color on client request
                rgbUpscale = "({},{},{})".format(round(rgbR),round(rgbG), round(rgbB) )
                print(rgbUpscale)
                #format the color into a hex code for output
                #and upscaled output on client request
                hexCode = '#{:02x}{:02x}{:02x}'.format(round(rgbR),round(rgbG), round(rgbB))
                deltaE = colorRGB.delta_e(rgbColor, method="2000")
                print(hexCode, rgbUpscale)
                print(deltaE , "NEW RGB\n\n")
                canRGB = True
                canRGBText = "Convertible"
            else:
                print("Not in RGB Gamut")
                before = colorRGB.in_gamut("a98-rgb")
                #fit color into correct gamut before continuing
                colorRGB.fit("a98-rgb")
                after = colorRGB.in_gamut("a98-rgb")
                print("before", before, "after", after)
                canRGB = False
                canRGBText = "Unconvertible"
                rgbColor = colorRGB.convert("a98-rgb")
                rgbR = rgbColor['r'] * 255
                rgbG = rgbColor['g'] * 255
                rgbB = rgbColor['b'] * 255
                #Upscale color on client request
                hexCode = '#{:02x}{:02x}{:02x}'.format(round(rgbR),round(rgbG), round(rgbB))
                rgbUpscale = "({},{},{})".format(round(rgbR),round(rgbG), round(rgbB) )
                deltaE = colorRGB.delta_e(rgbColor, method="2000")
                print(hexCode, rgbUpscale)
                print(deltaE , "NEW RGB\n\n")
            #check if color is in gamut (an appropriate conversion)
            if colorsRGB.in_gamut('srgb'):
                srgbColor = colorsRGB.convert("srgb")
                print(srgbColor)
                srgbR = srgbColor['r'] * 255
                srgbG = srgbColor['g'] * 255
                srgbB = srgbColor['b'] * 255
                #Upscale color on client request
                srgbUpscale = "({},{},{})".format(round(srgbR),round(srgbG), round(srgbB) )
                print(srgbUpscale)
                #format the color into a hex code for output
                #and upscaled output on client request
                shexCode = '#{:02x}{:02x}{:02x}'.format(round(srgbR),round(srgbG), round(srgbB))
                deltaE = colorsRGB.delta_e(srgbColor, method="2000")
                cansRGB = True
                cansRGBText = "Convertible"
                print(shexCode, srgbUpscale)
                print(deltaE , "NEW SRGB Y\n\n")
            else:
                print("Not in sRGB Gamut")
                before = colorsRGB.in_gamut('srgb')
                #fit color into correct gamut before continuing
                colorsRGB.fit('srgb')
                after = colorsRGB.in_gamut('srgb')
                print("before", before, "after", after)
                cansRGB = False
                cansRGBText = "Unconvertible"
                srgbColor = colorsRGB.convert("srgb")
                srgbR = srgbColor['r'] * 255
                srgbG = srgbColor['g'] * 255
                srgbB = srgbColor['b'] * 255
                #Upscale color on client request
                shexCode = '#{:02x}{:02x}{:02x}'.format(round(srgbR),round(srgbG), round(srgbB))
                srgbUpscale = "({},{},{})".format(round(srgbR),round(srgbG), round(srgbB) )
                deltaE = colorsRGB.delta_e(srgbColor, method="2000")
                print(shexCode, srgbUpscale)
                print(deltaE , "NEW SRGB N\n\n")
            #check if color is in gamut (an appropriate conversion)
            if colorPro.in_gamut('prophoto-rgb'):
                ProPhotoColor = colorPro.convert("prophoto-rgb")
                print(ProPhotoColor)
                ProR = ProPhotoColor['r'] * 255
                ProG = ProPhotoColor['g'] * 255
                ProB = ProPhotoColor['b'] * 255
                #print(rgbR,rgbG, rgbB )
                canPro = True
                canProText = "Convertible"
                proUpscale = "({},{},{})".format(round(ProR),round(ProG), round(ProB) )
                print(proUpscale)
                #format the color into a hex code for output
                #and upscaled output on client request
                ProHexCode = '#{:02x}{:02x}{:02x}'.format(round(ProR),round(ProG), round(ProB))
                deltaE = colorPro.delta_e(ProPhotoColor, method="2000")
                print(ProHexCode, proUpscale)
                print(deltaE , "NEW PROPHOTO\n\n")
            else:
                print("Not in ProPhoto Gamut")
                before = colorPro.in_gamut("prophoto-rgb")
                #fit color into correct gamut before continuing
                colorPro.fit("prophoto-rgb")
                after = colorPro.in_gamut("prophoto-rgb")
                print("before", before, "after", after)
                canPro = False
                canProText = "Unconvertible"
                ProPhotoColor = colorPro.convert("prophoto-rgb")
                ProR = ProPhotoColor['r'] * 255
                ProG = ProPhotoColor['g'] * 255
                ProB = ProPhotoColor['b'] * 255
                #Upscale color on client request
                ProHexCode = '#{:02x}{:02x}{:02x}'.format(round(ProR),round(ProG), round(ProB))
                proUpscale = "({},{},{})".format(round(ProR),round(ProG), round(ProB) )
                deltaE = colorPro.delta_e(ProPhotoColor, method="2000")
                print(ProHexCode, proUpscale)
                print(deltaE , "NEW PROPHOTO\n\n")
            '''
            #Check to make sure that the hex codes outputted are valid hex codes / the conversion was successful
            shexCodeCheck = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', shexCode)
            if not shexCodeCheck:
                shexCode = "#FFFFFF"
                cansRGB = False

            hexCodeCheck = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hexCode)
            if not hexCodeCheck:
                hexCode = "#FFFFFF"
                canRGB = False

            ProHexCodeCheck = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', ProHexCode)
            if not ProHexCodeCheck:
                ProHexCode = "#FFFFFF"
                canPro = False
            '''
            return render(request, 'pixelspace/colors.html', {'form':form, 'canRGB': canRGBText, 'hexCode': hexCode, 'rgb' : rgbUpscale, 'cansRGB': cansRGBText, 'shexCode': shexCode, 'srgb' : srgbUpscale, 'canPro': canProText, 'ProHexCode': ProHexCode, 'proUpscale' : proUpscale,})
    else:
        form=LABForm()

    return render(request, 'pixelspace/colors.html', {'form':form})

def URLConverter(img):
    output = BytesIO()
    img.save(output, format="PNG")
    imgData = output.getvalue()

    #encode the image data/ output of the image into base64 in order to pass it to an HTML page
    #and display the image to the user
    image_data = base64.b64encode(imgData)
    if not isinstance(image_data, str):
        # Python 3, decode from bytes to string
        image_data = image_data.decode()

    #format image data into HTML readable
    data_url = 'data:image/jpg;base64,' + image_data
    #print(data_url)
    return data_url

# was previously 'image'
def gallery(request):
    #locate gallery
    currGallery = gallery_collection.find_one(
        {'gallery':0}
    )
    #get dictionary
    urlID = {}
    arrayOfURLs = []
    #for every image that has been posted to the gallery
    for item in reversed(currGallery['gallery_images']):
        currMap = pixelmaps_collection.find_one(
            {'pixelmap_id':item}
        )

        mapWidth = currMap['width']
        #print(mapWidth)
        data = currMap['PixelMap']
        length = currMap['length']
        width = currMap['width']
        #take the binary encoding of the image and translate it back into an image object
        newImg = Image.frombytes("RGB",(length,width), data)
        #print(newImg)

        data_url = URLConverter(newImg)
        arrayOfURLs.append(data_url)
        #urlID.add(item,data_url)

        #Add to the dictionary of IDs and HTML readable URL to display
        urlID[item] = data_url
    #print(len(arrayOfURLs))
    #print(urlID.keys())
    #print(urlID.values())
    return render(request, 'pixelspace/gallery.html', {'gallery': urlID})

#processes the results of the pixelmap generation and displays it on a new page
def results(request):
    #grab the most recent pixelmap added to the database (the current one)
    newest_map = pixelmaps_collection.find_one(
        sort=[( '_id', pymongo.DESCENDING )]
        )

    data = newest_map['PixelMap']
    length = newest_map['length']
    width = newest_map['width']
    mapID = newest_map['pixelmap_id']

    '''
    #if the user is logged in, add this generated pixelmap (its ID) to their account
    if request.session['username']:
        username = request.session['username']
        users_collection.update_one({'username':username}, {'$push':{'pixelmap_ids':mapID}})
        print("UPDATED")
    '''
    #take the binary encoding of the image and translate it back into an image object
    newImg = Image.frombytes("RGB",(length,width), data)
    #print(newImg)

    #format image data into HTML readable
    data_url = URLConverter(newImg)

    #print(data_url)
    #data_url = 'data:image/jpg;base64,' + data
    #print("TESTING" , data_url)
    #binaryMap = newest_map[pixelmap]

    #if the saving form is valid, proceed
    if request.method == 'POST':
            print('testing1')
            form = SaveForm(request.POST)
            form2 = MapForm(request.POST)
            if form.is_valid() and form2.is_valid():
                print('testing')
                savePNG = form.cleaned_data.get("png")
                saveJPG = form.cleaned_data.get("jpg")
                saveTIF = form.cleaned_data.get("tif")

                deleteMap = form2.cleaned_data.get("deleteMap")
                submitMap = form2.cleaned_data.get("submitMap")

                #check to see what formats the user wants to save in, and make the necessary image saves
                if savePNG:
                    newImg.save("image.png")
                    print("png saved")
                if saveJPG:
                    newImg.save("image.jpeg")
                    print("jpg saved")
                if saveTIF:
                    newImg.save("image.tiff")
                    print("tiff saved")
                #if map delete is true, delete the map
                print("BEFORE SUBMIT", submitMap, deleteMap)
                if submitMap:
                    print("submitting...")
                    try:
                        request.session['username']
                        #insert pixelmap into database
                        newest_map = pixelmaps_collection.find_one(
                                sort=[( '_id', pymongo.DESCENDING )]
                        )
                        mapID = newest_map['pixelmap_id']
                        gallery_collection.update_one({'gallery':0}, {'$push':{'gallery_images':mapID}})
                        return redirect('image')

                    except:
                        return redirect('/pixelspace')

                if deleteMap:
                    print("testing3")
                    return redirect('delete-map-confirm')
                return render(request, 'pixelspace/results.html', {'form': form,'form2':form2, 'Image': data_url})
    else:
        form = SaveForm()
        form2 = MapForm()
        return render(request, 'pixelspace/results.html', {'form': form, 'form2':form2, 'Image': data_url})
    #return render(request, 'pixelspace/results.html', {'form': form, 'Image': data_url})

    '''
    if request.method == 'POST':
            print('testing1')
            form2 = MapForm(request.POST)
            if form2.is_valid():
                print('testing')
                deleteMap = form2.cleaned_data.get("deleteMap")

                if deleteMap:
                    print("testing3")
                    return redirect('delete-map-confirm')


            return render(request, 'pixelspace/results.html', {'form': form, 'Image': data_url})
    else:
        form = MapForm()
        return render(request, 'pixelspace/results.html', {'form': form, 'Image': data_url})
'''
def comment_delete(request, map_id=-1, pk=-1):
    if pk == -1 or map_id == -1:
        return redirect('/pixelspace')
    else:
        collection = dbname['comment']
        collection.delete_one({'ID':pk})
        print("DELETED COMMENT ID =", pk)
    # err
    return redirect('detail', map_id)

def detail(request, map_id):
        #check to see if User is logged in, if not, assign Guest User
        try:
            request.session['username']
            username = request.session['username']
        except:
            username = "Guest_User"

        mapID = map_id
        commentAuthor = []

        # grab the pixel map whose detail we want to view
        currMap = pixelmaps_collection.find_one(
            {'pixelmap_id':mapID}
        )

        data = currMap['PixelMap']
        length = currMap['length']
        width = currMap['width']

        #take the binary encoding of the image and translate it back into an image object
        newImg = Image.frombytes("RGB",(length,width), data)
        #print("NEW IMAGE:", newImg)

        data_url = URLConverter(newImg)

        # Find comments associated with current pixelmap
        currComments = comments_collection.find(
            {'pixelmap_id':mapID}
        )

        print("CURRENT COMMENTS:", currComments)

        #Create a list of tuples with the author name and the content of the comment
        #since multiple people can leave the same comment, and a person can leave more than one comment
        #a dictionary is infeasible for this task
        for item in currComments:
            #print(item)
            commentAuthor.append((item['author'], item['content'], item['ID']))
            #commentAuthor[item] = data_url

    #    for author, comment, ID in commentAuthor:
    #        print(author, comment, ID)

        #retrieve current amount of likes to be displayed
        currMap = pixelmaps_collection.find_one(
            {'pixelmap_id':mapID}
        )
        currMapLikes = int(currMap["likes"])

        if request.method == 'POST':
            comment_form = commentForm(request.POST)
            like_form = LikeForm(request.POST)
            #handle liking
            if like_form.is_valid():
                #print("liking..")
                #increment the amount of likes, and update it in the database
                currMapLikes = currMapLikes + 1
                pixelmaps_collection.update_one({'pixelmap_id':mapID}, {'$set':{'likes':currMapLikes}})
                return render(request, 'pixelspace/detail.html', {'form':comment_form ,'form2':like_form ,'mapID':mapID, 'dataURL': data_url, 'commentAuthor': commentAuthor, 'currMapLikes': currMapLikes})

            #if the button is not pressed, return empty form
            elif not like_form.is_valid():
                like_form = LikeForm()

            #handles commenting
            if comment_form.is_valid():
                newestComment = comments_collection.find_one(
                    sort=[( '_id', pymongo.DESCENDING )]
                )

                try:
                    newest_comment_id = int(newestComment["ID"]) + 1
                except:
                    # if the db has no comments yet
                    newest_comment_id = 0

                #get content from user, and add a comment to the database
                content = comment_form.cleaned_data.get("content")
                comment = {
                    "ID": newest_comment_id,
                    "author" : username,
                    "content" : content,
                    "pixelmap_id" : mapID,
                }
                comments_collection.insert_one(comment)

                print(comment_form , like_form, data_url, commentAuthor, currMapLikes)

                commentAuthor.append((comment['author'], comment['content'], comment['ID']))

                return render(request, 'pixelspace/detail.html', {'form':comment_form , 'form2':like_form, 'mapID':mapID, 'dataURL': data_url, 'commentAuthor': commentAuthor, 'currMapLikes': currMapLikes})
            else:
                comment_form = commentForm()
                return render(request, 'pixelspace/detail.html', {'form':comment_form , 'form2':like_form, 'dataURL': data_url,  'commentAuthor': commentAuthor})
        else:
            comment_form = commentForm()
            like_form = LikeForm()
            return render(request, 'pixelspace/detail.html', {'form':comment_form , 'form2':like_form , 'mapID':mapID, 'dataURL': data_url,  'commentAuthor': commentAuthor, 'currMapLikes': currMapLikes})

        #return HttpResponse("You're looking at map %s." % map_id)
        return render(request, 'pixelspace/detail.html', {'mapID':mapID, 'dataURL': data_url, 'commentAuthor': commentAuthor})

def login(request):

    template = loader.get_template('pixelspace/login.html')
    if request.method == 'POST':
        form = UserForm(request.POST)
        #acquire login and password from user input
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print("provided USER:", username, "\nprovided PASSWORD:", password)

            # authenticate credentials
            user = mongo_auth.authenticate(username=username, password=password)

            if user:
                # log user into the session
                mongo_auth.login(request, user)
                #messages.success(request, "LOGGED IN ALERT") # WIP !!!!!!!!!!!
                messages.add_message(request, messages.SUCCESS, 'Sucessfully Logged In') #, extra_tags='login_alert')

                print("Successfully logged in user:", user['username'])
                return redirect('/pixelspace')
            else:
                print("ERROR: Incorrect Credentials", username)
                return render(
                    request,
                    'pixelspace/login.html',
                    {'form':form},
                    status=HTTPStatus.BAD_REQUEST,
                )
    else:
        form = UserForm()
    return render(request, 'pixelspace/login.html', {'form':form})

#Log out Function
def logout(request):
    #if the user is authenticated when logout() is called, log them out
    try:
        if request.session['username']:
            print("Successfully logged out user:", request.session['username'])
            del request.session['username']
            return redirect('/pixelspace')
    except:
        return render(
            request,
            'pixelspace/login.html',
            status=HTTPStatus.FOUND,
        )

def logo(request):
    template = loader.get_template('pixelspace/logo.html')
    #return HttpResponse(template.render(request))
    print("here")
    if request.method == "POST":
        print("also here")
        #initialize forms
        form = ShapeForm(request.POST)
        form2 = RectangleForm()
        form3 = OvalForm()
        form4 = PolyForm()
        data_url = ""
        #obtain the shape chosen, and store it into a hidden variable so that it can be passed onto subsequent forms
        if form.is_valid():
            shape = form.cleaned_data.get("shape")
            print(shape)
            #For each shape, request information from that form, and pass empty forms for the other shapes
            if shape == "rectangle":
                form2 = RectangleForm(request.POST)
                form3 = OvalForm()
                form4 = PolyForm()
                if form2.is_valid():
                    logoLen = form2.cleaned_data.get("logoLen")
                    logoWid = form2.cleaned_data.get("logoWid")
                    color = form2.cleaned_data.get("color")
                    text = form2.cleaned_data.get("text")
                    textColor = form2.cleaned_data.get("textColor")
                    print(logoLen, shape, logoWid)
                    #make the border of the image slightly larger than the shape
                    scaledLBorder = int(logoLen * 0.2) + logoLen
                    scaledWBorder = int(logoWid * 0.2) + logoWid
                    img = Image.new('RGB', [scaledLBorder,scaledWBorder], 'white')
                    #create the bounding box for the shape. Start the top left point a few pixels away from the edge of the image
                    #And place the bottom right point length and width number of pixels away to make a shape of the specified size
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([(int(logoLen * 0.1),int(logoWid * 0.1)), (int(logoLen * 0.1) + logoLen, int(logoWid * 0.1) + logoWid)], fill=color)

                    if logoLen < logoWid:
                        fontsize = int(logoLen/4)
                    else:
                        fontsize = int(logoWid/4)
                    font = ImageFont.truetype("arial.ttf", fontsize)
                    
                    #_,_,length, width = draw3.textbbox((0,0),text, font=font)
                    newL= int((scaledLBorder/2))
                    newW = int((scaledWBorder/2))
                    #print(newL,newW)
                    draw.text((newL,newW), text, fill=textColor,font=font, align='center', anchor='mm')
                    img.show()
                    #convert to URL to be displayed
                    data_url = URLConverter(img)
                    
                else:
                    form2 = RectangleForm()
                            
            elif shape == "oval":
                form2 = RectangleForm()
                form3 = OvalForm(request.POST)
                form4 = PolyForm()
                if form3.is_valid():
                    ovalLen = form3.cleaned_data.get("ovalLen")
                    ovalWid = form3.cleaned_data.get("ovalWid")
                    color = form3.cleaned_data.get("color")
                    text = form3.cleaned_data.get("text")
                    textColor = form3.cleaned_data.get("textColor")
                    print(ovalLen, ovalWid)
                    #make the border of the image slightly larger than the shape
                    scaledLBorder = int(ovalLen * 0.2) + ovalLen
                    scaledWBorder = int(ovalWid * 0.2) + ovalWid
                    imgOval = Image.new('RGB', [scaledLBorder,scaledWBorder], 'white')

                    #create the bounding box for the shape. Start the top left point a few pixels away from the edge of the image
                    #And place the bottom right point length and width number of pixels away to make a shape of the specified size
                    draw3 = ImageDraw.Draw(imgOval)
                    draw3.ellipse((int(ovalLen * 0.2),int(ovalWid * 0.2),ovalLen,ovalWid), fill=color)
                    meow = ovalWid - int(ovalWid * 0.2)
                    print("orange: ", meow )
                    if ovalLen < ovalWid:
                        fontsize = int(ovalLen/4)
                    else:
                        fontsize = int(ovalWid/4)
                    font = ImageFont.truetype("arial.ttf", fontsize)
                    
                    #_,_,length, width = draw3.textbbox((0,0),text, font=font)
                    newL= int((scaledLBorder/2))
                    newW = int((scaledWBorder/2))
                    #print(newL,newW)
                    draw3.text((newL,newW), text, fill=textColor,font=font, align='center', anchor='mm')

                    #draw.rectangle([(int(diameter * 0.1),int(logoWid * 0.1)), (int(diameter * 0.1) + diameter, int(logoWid * 0.1) + logoWid)], fill=color)

                    imgOval.show()
                    data_url = URLConverter(imgOval)
                else:
                    form3 = OvalForm()
            elif shape == "polygon":
                form2 = RectangleForm()
                form3 = OvalForm()
                form4 = PolyForm(request.POST)
                if form4.is_valid():
                    polySize = form4.cleaned_data.get("polySize")
                    noSides = form4.cleaned_data.get("noSides")
                    color = form4.cleaned_data.get("color")
                    text = form4.cleaned_data.get("text")
                    textColor = form4.cleaned_data.get("textColor")
                    print(polySize,noSides)
                    #make the border of the image slightly larger than the shape
                    scaledLBorder = int(polySize * 0.2 + polySize)
                    scaledWBorder = int(polySize * 0.2 + polySize)
                    imgPoly = Image.new('RGB', [polySize *2,polySize *2], 'white')

                    draw2 = ImageDraw.Draw(imgPoly)
                    draw2.regular_polygon((polySize,polySize, polySize), noSides, fill=color)

                    fontsize = int(polySize/4)
                    font = ImageFont.truetype("arial.ttf", fontsize)
                    print(polySize)
                    #_,_,length, width = draw3.textbbox((0,0),text, font=font)
                    newL= int((polySize))
                    newW = int((polySize))
                    #print(newL,newW)
                    draw2.text((newL,newW), text, fill=textColor,font=font, align='center', anchor='mm')

                    imgPoly.show()
                    data_url = URLConverter(imgPoly)
                else:
                    form4 = PolyForm()

        else:
            form2 = RectangleForm()
            form3 = OvalForm()
            form4 = PolyForm()
            data_url = ""
        return render(request, 'pixelspace/logo.html', {'form': form,'form2': form2,'form3': form3,'form4': form4,  'shape':shape, 'data_url':data_url})
        #return render(request, 'pixelspace/logo.html', {'form': form,'form2': form2,'form3': form3,'form4': form4})
    else:
        form = ShapeForm()
        form2 = RectangleForm()
        form3 = OvalForm()
        form4 = PolyForm()

    return render(request, 'pixelspace/logo.html', {'form': form, 'form2': form2,'form3': form3,'form4': form4,})



def pixelmap(request):
    template = loader.get_template('pixelspace/pixelmap.html')

    #set username to username or guest username depending on if the user is logged in
    try:
        request.session['username']
        username = request.session['username']
    except:
        username = "Guest_User"
    if request.method == 'POST':
            form = PixelForm(request.POST)
            #form2 = CustomForm(request.POST)
            #acquire acquire length, width, and greyscale from user input
            if form.is_valid():
                length = form.cleaned_data.get("length")
                width = form.cleaned_data.get("width")
                greyscale = form.cleaned_data.get("greyscale")

                rrangeLow = form.cleaned_data.get("rrangeLow")
                grangeLow = form.cleaned_data.get("grangeLow")
                brangeLow = form.cleaned_data.get("brangeLow")

                rrangeHigh = form.cleaned_data.get("rrangeHigh")
                grangeHigh = form.cleaned_data.get("grangeHigh")
                brangeHigh = form.cleaned_data.get("brangeHigh")

                custom = form.cleaned_data.get("custom")


                print("provided length:", length, "\nprovided width:", width)
                print(custom, "provided length:", rrangeLow, "\nprovided width:", rrangeHigh)

                #generate placeholder image in which to fill in with pixels
                img = Image.new('RGB', [length,width], 'pink')

                #the process is similar for if the maps are greyscale or color
                #generate a random value between 1-255, and apply to rgb balues
                #append onto a list of values, which then gets mapped to the image
                if custom == True:
                    colorRange = [rrangeLow,brangeLow,grangeLow,rrangeHigh,brangeHigh,grangeHigh]
                    for item in range(len(colorRange)):
                        if colorRange[item] == None and item < 3:
                            print(colorRange[item])
                            colorRange[item] = 1
                        if colorRange[item] == None and item >= 3:
                            print(colorRange[item])
                            colorRange[item] = 255
                    listCustom= [0] * (width * length )
                    for x in range(width * length ):
                        r = random.randint(colorRange[0],colorRange[3])
                        g = random.randint(colorRange[2],colorRange[5])
                        b = random.randint(colorRange[1],colorRange[4])
                        listCustom[x] = (r,g,b)
                    img.putdata(listCustom)
                    img.show()

                elif greyscale == True:
                    listGrey= [0] * (width * length )
                    for x in range(width * length ):
                        Grey = random.randint(1,255)
                        listGrey[x] = (Grey,Grey,Grey)
                    img.putdata(listGrey)
                    img.show()
                else:
                    listColor= [0] * (width * length )
                    for x in range(width * length ):
                        r = random.randint(1,255)
                        g = random.randint(1,255)
                        b = random.randint(1,255)
                        listColor[x] = (r,g,b)
                    img.putdata(listColor)
                    img.show()

                #get the previous map
                newest_map = pixelmaps_collection.find_one(
                    sort=[( '_id', pymongo.DESCENDING )]
                )

                #increment the id of the previous map to get the id for the current map
                newest_map_id = int(newest_map["pixelmap_id"]) + 1

                #convert image to binary in order to store in the database
                bin = img.tobytes()

                #insert pixelmap into database
                pixelmap = {
                    "pixelmap_id": newest_map_id,
                    "creator" : username,
                    "caption" : "temp",
                    "PixelMap" : bin,
                    "width" : width,
                    "length" : length,
                    "likes" : 0,
                    }
                pixelmaps_collection.insert_one(pixelmap)

                #if the user is logged in, add this generated pixelmap (its ID) to their account
                try:
                    username = request.session['username']
                    users_collection.update_one({'username':username}, {'$push':{'pixelmap_ids':newest_map_id}})
                    print("UPDATED")
                except:
                    print("As Guest")

                print("PixelMap successfully created")
                #return results(request, data_url, img)
                return redirect('results')
                #return render(request, 'pixelspace/results.html', {'form':form, 'Image': data_url})

    else:
        form = PixelForm()

    return render(request, 'pixelspace/pixelmap.html', {'form':form})

# need to tEST
def deleteConfirm(request):
    #currAcc = User.objects.get(username = request.user.username)
    try:
        request.session['username']
    except:
        return redirect('/pixelspace')

    username = request.session['username']

    curr_account = users_collection.find_one(
        {'username':username}
    )

    form = confirmDeleteForm(request.POST)
    if form.is_valid():
        confirmDelete = form.cleaned_data.get("confirmDelete")
        if confirmDelete:
            #users_collection.delete_one({'username':username})
            mongo_auth.delete_user(username, "users")

            del request.session['username']
            return redirect('/pixelspace')

    return render(request, 'pixelspace/delete-confirm.html', {'form':form})

def deleteMapConfirm(request):
    #currAcc = User.objects.get(username = request.user.username)
    #check to make sure user is logged in
    try:
        request.session['username']
    except:
        return redirect('/pixelspace')

    username = request.session['username']

    curr_account = users_collection.find_one(
        {'username':username}
    )

    newest_map = pixelmaps_collection.find_one(
        sort=[( '_id', pymongo.DESCENDING )]
        )

    mapID = newest_map['pixelmap_id']
    #confirm that the map is deleted properly (the box is ticked)
    form = confirmMapDeleteForm(request.POST)
    if form.is_valid():
        confirmMapDelete = form.cleaned_data.get("confirmMapDelete")
        #delete from map and delete from user's owned maps array
        if confirmMapDelete:
            print("Successfully deleted Map", mapID)
            pixelmaps_collection.delete_one({'pixelmap_id':mapID})
            users_collection.update_one({'username':username}, {'$pop':{'pixelmap_ids':1}})


            return redirect('/pixelspace')

    return render(request, 'pixelspace/delete-map-confirm.html', {'form':form})

#Settings, currently has change password functionality
def settings(request):
    if request.method == 'POST':
        #grab the password to change to
        form = SettingsForm(request.POST)
        if form.is_valid():
            changedPassword = form.cleaned_data.get("newPassword")
            retypePassword = form.cleaned_data.get("retypePassword")
            deleteAccount = form.cleaned_data.get("deleteAccount")

            try:
                if request.session['username']:
                    username = request.session['username']

                    curr_account = users_collection.find_one(
                        {'username':username}
                    )

                # user can confirm that they want to delete their account
                if deleteAccount:
                    return redirect('delete-confirm')

                #if the password matches the confirmation password, go through with the change
                if changedPassword and changedPassword == retypePassword:
                    print("* The new passwords match *")
                    #when the password is changed, log user out and direct them to the homepage
                    mongo_auth.change_password("users", username, changedPassword)
                    print("Successfully updated settings for:", username)
                    return logout(request)
                else:
                    print("* The new passwords do not match *")
            except:
                return redirect('login')
        else:
            print("* Invalid settings form *")
    else:
        form = SettingsForm()
    return render(request, 'pixelspace/settings.html', {'form':form})

def create_account(request):
    template = loader.get_template('pixelspace/create_account.html')
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            # obtain the new username and new password information from the form
            new_username = form.cleaned_data.get("username")
            new_password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")
            new_email = form.cleaned_data.get("email")

            # ! ERROR CHECK INPUT HERE (or in form?) !

            print(f'NEW USER: {new_username} \n NEW_PASS: {new_password} \n CON_PASS: {confirm_password} \n EMAIL: {new_email}')

            if mongo_auth.already_exists("users", new_username):
                # ! DISPLAY ERROR NOTIFICATION TO USER !
                print("An Account with that Username Already Exists")
                return redirect('create-account')

            # If the input is valid, create a new user
            elif new_password == confirm_password:
                mongo_auth.create_account(
                    new_username,
                    new_password,
                    new_email,
                    "users"
                )
                return redirect('login')
            else:
                print("Error: passwords did not match")
                messages.error(request, 'Passwords did not match.')
                return redirect('create-account')

            return redirect('/pixelspace/login')
    else:
        form=AccountForm()

    return render(request, 'pixelspace/create_account.html', {'form':form})
