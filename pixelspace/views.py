from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import base64
from http import HTTPStatus
import os, sys
from django.contrib.auth.decorators import login_required
from .forms import AccountForm, UserForm, SettingsForm, LABForm, confirmDeleteForm, PixelForm
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

# ! CAN'T use authenticate() WIP !

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
            colorrr = Color("lab", testing)
            print(colorrr)
            #check if color is in gamut (an appropriate conversion)
            if colorrr.in_gamut('a98-rgb'):
                rgbColor = colorrr.convert("a98-rgb")
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
                deltaE = colorrr.delta_e(rgbColor, method="2000")
                print(hexCode, rgbUpscale)
                print(deltaE , "NEW RGB\n\n")
                canRGB = True
            else:
                print("Not in RGB Gamut")
                before = colorrr.in_gamut("a98-rgb")
                #fit color into correct gamut before continuing
                colorrr.fit("a98-rgb")
                after = colorrr.in_gamut("a98-rgb")
                print("before", before, "after", after)
                canRGB = False
                rgbColor = colorrr.convert("a98-rgb")
                rgbR = rgbColor['r'] * 255
                rgbG = rgbColor['g'] * 255
                rgbB = rgbColor['b'] * 255
                #Upscale color on client request
                hexCode = '#{:02x}{:02x}{:02x}'.format(round(rgbR),round(rgbG), round(rgbB))
                rgbUpscale = "({},{},{})".format(round(rgbR),round(rgbG), round(rgbB) )
                deltaE = colorrr.delta_e(rgbColor, method="2000")
                print(hexCode, rgbUpscale)
                print(deltaE , "NEW RGB\n\n")
            #check if color is in gamut (an appropriate conversion)
            if colorrr.in_gamut('srgb'):
                srgbColor = colorrr.convert("srgb")
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
                deltaE = colorrr.delta_e(srgbColor, method="2000")
                cansRGB = True
                print(shexCode, srgbUpscale)
                print(deltaE , "NEW SRGB Y\n\n")
            else:
                print("Not in sRGB Gamut")
                before = colorrr.in_gamut('srgb')
                #fit color into correct gamut before continuing
                colorrr.fit('srgb')
                after = colorrr.in_gamut('srgb')
                print("before", before, "after", after)
                cansRGB = False
                srgbColor = colorrr.convert("srgb")
                srgbR = srgbColor['r'] * 255
                srgbG = srgbColor['g'] * 255
                srgbB = srgbColor['b'] * 255
                #Upscale color on client request
                shexCode = '#{:02x}{:02x}{:02x}'.format(round(srgbR),round(srgbG), round(srgbB))
                srgbUpscale = "({},{},{})".format(round(srgbR),round(srgbG), round(srgbB) )
                deltaE = colorrr.delta_e(srgbColor, method="2000")
                print(shexCode, srgbUpscale)
                print(deltaE , "NEW SRGB N\n\n")
            #check if color is in gamut (an appropriate conversion)
            if colorrr.in_gamut('prophoto-rgb'):
                ProPhotoColor = colorrr.convert("prophoto-rgb")
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
                deltaE = colorrr.delta_e(ProPhotoColor, method="2000")
                print(ProHexCode, proUpscale)
                print(deltaE , "NEW PROPHOTO\n\n")
            else:
                print("Not in ProPhoto Gamut")
                before = colorrr.in_gamut("prophoto-rgb")
                #fit color into correct gamut before continuing
                colorrr.fit("prophoto-rgb")
                after = colorrr.in_gamut("prophoto-rgb")
                print("before", before, "after", after)
                canPro = False
                ProPhotoColor = colorrr.convert("prophoto-rgb")
                ProR = ProPhotoColor['r'] * 255
                ProG = ProPhotoColor['g'] * 255
                ProB = ProPhotoColor['b'] * 255
                #Upscale color on client request
                ProHexCode = '#{:02x}{:02x}{:02x}'.format(round(ProR),round(ProG), round(ProB))
                srgbUpscale = "({},{},{})".format(round(ProR),round(ProG), round(ProB) )
                deltaE = colorrr.delta_e(ProPhotoColor, method="2000")
                print(ProHexCode, proUpscale)
                print(deltaE , "NEW PROPHOTO\n\n")

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

            return render(request, 'pixelspace/colors.html', {'form':form, 'canRGB': canRGB, 'hexCode': hexCode, 'rgb' : rgbUpscale, 'cansRGB': cansRGB, 'shexCode': shexCode, 'srgb' : srgbUpscale, 'canPro': canPro, 'ProHexCode': ProHexCode, 'proUpscale' : proUpscale,})
    else:
        form=LABForm()

    return render(request, 'pixelspace/colors.html', {'form':form})

def image(request):
    template = loader.get_template('pixelspace/image.html')
    #return HttpResponse(template.render(request))
    latest_question_list = [1]
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

#login function
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
    if request.session['username']:
        username = request.session['username']
    else:
        username = "Guest_User"
    if request.method == 'POST':
            form = PixelForm(request.POST)
            #acquire login and password from user input
            if form.is_valid():
                length = form.cleaned_data.get("length")
                width = form.cleaned_data.get("width")
                greyscale = form.cleaned_data.get("greyscale")
                print("provided length:", length, "\nprovided width:", width)
                img = Image.new('RGB', [length,width], 'pink')

                if greyscale == True:
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


                newest_map = pixelmaps_collection.find_one(
                    sort=[( '_id', pymongo.DESCENDING )]
                )

                newest_map_id = int(newest_map["pixelmap_id"]) + 1
                bin = img.tobytes("xbm", "rgb")

                output = BytesIO()
                img.save(output, format="PNG")
                imgData = output.getvalue()

                image_data = base64.b64encode(imgData)
                if not isinstance(image_data, str):
                    # Python 3, decode from bytes to string
                    image_data = image_data.decode()
                data_url = 'data:image/jpg;base64,' + image_data                
                print(img)
                pixelmap = {
                    "pixelmap_id": newest_map_id,
                    "creator" : username,
                    "caption" : "temp",
                    "PixelMap" : bin,
                    }
                pixelmaps_collection.insert_one(pixelmap)

                print("PixelMap successfully created")
                return render(request, 'pixelspace/results.html', {'form':form, 'Image': data_url})
                
    else:
        form = PixelForm()
    return render(request, 'pixelspace/pixelmap.html', {'form':form})

# need to tEST
def deleteConfirm(request):
    #currAcc = User.objects.get(username = request.user.username)

    if not request.session['username']:
        return redirect('/pixelspace')

    username = request.session['username']

    curr_account = users_collection.find_one(
        {'username':username}
    )

    form = confirmDeleteForm(request.POST)
    if form.is_valid():
        confirmDelete = form.cleaned_data.get("confirmDelete")
        if confirmDelete:
            print("Successfully deleted user:", username)
            users_collection.delete_one({'username':username})

            del request.session['username']
            return redirect('/pixelspace')

    return render(request, 'pixelspace/delete-confirm.html', {'form':form})

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

                if deleteAccount:
                    # ! ASK USER TO CONFIRM THAT THEY WANT TO DELETE FIRST !
                    return redirect('delete-confirm')

                #if the password matches the confirmation password, go through with the change
                if changedPassword and changedPassword == retypePassword:

                    # ! ERROR CHECK NEW PASSWORDS HERE !

                    print("* The new passwords match *")
                    #when the password is changed, log user out and direct them to the homepage
                    users_collection.update_one({'username':username}, {'$set':{'password':changedPassword}})
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
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            #obtain the new username and new password information from the form
            new_username = form.cleaned_data.get("newUser")
            new_password = form.cleaned_data.get("newPass")
            confirm_password = form.cleaned_data.get("confirmPass")

            # ! ERROR CHECK INPUT HERE (or in form?) !

            print(new_username, new_password, confirm_password)

            already_exists = users_collection.find_one(
                {'username':new_username}
            )

            if already_exists:
                # ! DISPLAY ERROR NOTIFICATION TO USER !
                print("ERROR: An account with this username already exists")
                return redirect('create-account')

            # If the input is valid, create a new user
            elif new_password == confirm_password:
                newest_user = users_collection.find_one(
                    sort=[( '_id', pymongo.DESCENDING )]
                )

                new_user_id = int(newest_user["user_id"]) + 1

                new_user = {
                    "user_id": new_user_id,
                    "username" : new_username,
                    "password" : new_password,
                    "email" : "bag@gmail.com",
                }

                users_collection.insert_one(new_user)

                print("Account successfully created")
                return redirect('login')
            else:
                print("Error: passwords did not match")
                messages.error(request, 'Passwords did not match.')
                return redirect('create-account')

            return redirect('/pixelspace/login')
    else:
        form=UserForm()

    return render(request, 'pixelspace/create_account.html', {'form':form})
