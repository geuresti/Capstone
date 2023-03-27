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
from .forms import AccountForm, UserForm, SettingsForm, LABForm, confirmDeleteForm, PixelForm, SaveForm, MapForm, confirmMapDeleteForm, CustomForm
from django.contrib import messages
from colormath.color_objects import LabColor, sRGBColor, AdobeRGBColor
from colormath.color_objects import BT2020Color
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976
from coloraide.everything import ColorAll as Color
import pymongo
from PIL import Image
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
            else:
                print("Not in RGB Gamut")
                before = colorRGB.in_gamut("a98-rgb")
                #fit color into correct gamut before continuing
                colorRGB.fit("a98-rgb")
                after = colorRGB.in_gamut("a98-rgb")
                print("before", before, "after", after)
                canRGB = False
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
            return render(request, 'pixelspace/colors.html', {'form':form, 'canRGB': canRGB, 'hexCode': hexCode, 'rgb' : rgbUpscale, 'cansRGB': cansRGB, 'shexCode': shexCode, 'srgb' : srgbUpscale, 'canPro': canPro, 'ProHexCode': ProHexCode, 'proUpscale' : proUpscale,})
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
    print(data_url)
    return data_url

def image(request):
    template = loader.get_template('pixelspace/image.html')
    #return HttpResponse(template.render(request))
    latest_question_list = [1]
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

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

    #format image data into HTML readable
    data_url = URLConverter(newImg)


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

# MESSAGES WIP
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
    latest_question_list = [1]
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

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
