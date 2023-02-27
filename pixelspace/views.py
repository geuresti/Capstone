from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from .models import Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from .forms import AccountForm, UserForm, SettingsForm, LABForm, CreateAccountForm, confirmDeleteForm
from django.contrib import messages
from colormath.color_objects import LabColor, sRGBColor, AdobeRGBColor
from colormath.color_objects import BT2020Color
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976
import re

def index(request):

    template = loader.get_template('pixelspace/index.html')

    latest_question_list = [1]
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

#View Function for the Colors template
def colors(request):
    template = loader.get_template('pixelspace/colors.html')
    if request.method == 'POST':
        #take in L*A*B values
        form = LABForm(request.POST)
        #if the inputs are valid
        if form.is_valid():
            print("in")
            #assign form values to variables
            lightness1 = form.cleaned_data.get("lightness")
            axisA = form.cleaned_data.get("axisA")
            axisB = form.cleaned_data.get("axisB")
            testing = [lightness1, axisA, axisB]
            print(lightness1,axisA,axisB)
            #Initialize boolean of whether value can be converted
            canRGB = False
            cansRGB = False
            canBT = False
            lab = LabColor(lightness1, axisA, axisB)
            #RGB conversion
            try:
                rgb = convert_color(lab, AdobeRGBColor)
                print(rgb)
                canRGB =  True
                #format the color into a hex code for output
                #and upscaled output on client request
                hexCode = rgb.get_rgb_hex()
                rgbUpscale = rgb.get_upscaled_value_tuple()
                print(rgbUpscale)
                #colors = [red,green,blue]
            except:
                canRGB = False
                hexCode = "#FFFFFF"
                rgb = "Not Applicable"
            #sRGB conversion
            try:
                srgb = convert_color(lab, sRGBColor)
                print(srgb)
                cansRGB =  True
                #format the color into a hex code for output
                #and upscaled output on client request
                shexCode = srgb.get_rgb_hex()
                srgbUpscale = srgb.get_upscaled_value_tuple()
                #colors = [red,green,blue]
            except:
                cansRGB = False
                shexCode = "#FFFFFF"
                srgb = "Not Applicable"
            #BTColor conversion
            try:
                btcolor = convert_color(lab, BT2020Color)
                print(btcolor)
                canBT =  True
                #format the color into a hex code for output
                #and upscaled output on client request
                BTHexCode = btcolor.get_rgb_hex()
                BTUpscale = btcolor.get_upscaled_value_tuple()
                #btcolor = [red,green,blue]
            except:
                canBT = False
                BTHexCode = "#FFFFFF"
                btcolor = "Not Applicable"

            #Check to make sure that the hex codes outputted are valid hex codes / the conversion was successful
            shexCodeCheck = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', shexCode)
            if not shexCodeCheck:
                shexCode = "#FFFFFF"
                cansRGB = False

            hexCodeCheck = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hexCode)
            if not hexCodeCheck:
                hexCode = "#FFFFFF"
                canRGB = False

            BTHexCodeCheck = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', BTHexCode)
            if not hexCodeCheck:
                BTHexCode = "#FFFFFF"
                canBT = False

            return render(request, 'pixelspace/colors.html', {'form':form, 'canRGB': canRGB, 'hexCode': hexCode, 'rgb' : rgbUpscale, 'cansRGB': cansRGB, 'shexCode': shexCode, 'srgb' : srgbUpscale, 'canBT': canBT, 'BTHexCode': BTHexCode, 'btcolor' : BTUpscale,})
    else:
        print("NO")
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
            print("USER:", username, "\nPASSWORD:", password)
            #if username exists in the database
            if User.objects.filter(username=username).exists():
                #make sure the user can be authentificated
                user = authenticate(request, username=username, password=password)
                if user:
                    #log the user in and redirect to the homepage
                    dj_login(request, user)
                    print("Successful login for user:", username)
                    return redirect('/pixelspace')
                else:
                    print("Unsuccessful login: incorrect password")
            else:
                print("ERROR: No account found with username =", username)
            return render(request, 'pixelspace/login.html', {'form':form})
    else:
        form = UserForm()
    return render(request, 'pixelspace/login.html', {'form':form})

#Log out Function
def logout(request):
    #if the user is authenticated when the logout function is called, log them out
    if request.user.is_authenticated:
        print("Successfully logged out user:", request.user.username)
        dj_logout(request)
    return redirect('/pixelspace')

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
    #return HttpResponse(template.render(request))
    latest_question_list = [1]
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def deleteConfirm(request):
    currAcc = User.objects.get(username = request.user.username)
    form = confirmDeleteForm(request.POST)
    if form.is_valid():
        confirmDelete = form.cleaned_data.get("confirmDelete")
        if confirmDelete:
            print("Successfully deleted user:", currAcc.username)
            currAcc.delete()
            return redirect('login')
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

            print("changedPassword:",
                changedPassword,
                "\nretypePassword:",
                retypePassword,
                "\ndeleteAccount:",
                deleteAccount)

            currAcc = User.objects.get(username = request.user.username)

            if deleteAccount:
                # ! ASK USER TO CONFIRM THAT THEY WANT TO DELETE FIRST !
                return redirect('delete-confirm')

            #if the password matches the confirmation password, go through with the change
            if changedPassword and changedPassword == retypePassword:

                # ! ERROR CHECK NEW PASSWORDS HERE !

                print("* The new passwords match *")
                #when the password is changed, log user out and direct them to the homepage
                #for acc in currAcc:
                currAcc.set_password(changedPassword)
                currAcc.save()
                print(currAcc.username, currAcc.password)
                print("Successfully updated settings for:", currAcc.username)
                return logout(request)
            else:
                print("* The new passwords do not match *")
        else:
            print("* Invalid settings form *")
    else:
        print("REQUEST = GET for settings view")
        form = SettingsForm()
    return render(request, 'pixelspace/settings.html', {'form':form})

def create_account(request):
    template = loader.get_template('pixelspace/create_account.html')
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            #obtain the new username and new password information from the form
            newUser= form.cleaned_data.get("newUser")
            newPass= form.cleaned_data.get("newPass")
            confirmPass = form.cleaned_data.get("confirmPass")

            # ! ERROR CHECK INPUT HERE !

            #print(newUser,newPass, confirmPass)

            currAcc = User.objects.filter(username = newUser)
            if currAcc:

                # ! DISPLAY ERROR NOTIFICATION TO USER !

                print("ERROR: An account with this username already exists")
                return redirect('create-account')

            # If the input is valid, create a new user
            if newPass == confirmPass:

                user = User.objects.create_user(
                    username=newUser,
                    password=newPass,
                )

            else:
                print("Error: passwords did not match")
                messages.error(request, 'Passwords did not match.')
                return redirect('create-account')

            return redirect('/pixelspace/login')
    else:
        print("NO")
        form=UserForm()

    #print(form)
    return render(request, 'pixelspace/create_account.html', {'form':form})
