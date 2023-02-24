from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from .models import Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login, logout
from django.contrib.auth.decorators import login_required
from .forms import AccountForm
from .forms import NameForm
from .forms import changeForm
from .forms import LABForm
from .forms import CreateAccountForm
from django.contrib import messages
from colormath.color_objects import LabColor, sRGBColor, AdobeRGBColor
from colormath.color_objects import BT2020Color
from colormath.color_conversions import convert_color
import re
from colormath.color_diff import delta_e_cie1976

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
        form = NameForm(request.POST)
        #acquire login and password from user input
        if form.is_valid():
            print("in")
            usern= form.cleaned_data.get("username")
            password1= form.cleaned_data.get("password")
            #initialize boolean to check if account exists
            accountValid = False
            print(usern,password1)
            #if username exists in the database
            if User.objects.filter(username=usern).exists():
                print("valid account")
                accountValid = True
                #make sure the user can be authentificated
                user = authenticate(request, username =usern, password=password1)
                if user:
                    #log the user in and redirect to the homepage
                    dj_login(request, user)
                    return redirect('/pixelspace')

                else:
                    print("invalid account1")
            else:
                print("invalid account2")
            return render(request, 'pixelspace/login.html', {'form':form, 'accountValid' : accountValid})
    else:
        print("NO")
        form=NameForm()
    return render(request, 'pixelspace/login.html', {'form':form})

#Log out Function
def LoggingOut(request):
    #if the user is authenticated when the logout function is called, log them out and redirect to the homepage
    if request.user.is_authenticated:
        logout(request)
        return redirect('/pixelspace')
    else:
        print("nop.")

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

#Settings, currently has change password functionality
def settings(request):
    if request.method == 'POST':
        #grab the password to change to
        form = changeForm(request.POST)
        if form.is_valid():
            print("in")
            changedPassword= form.cleaned_data.get("newPassword")
            retypePassword= form.cleaned_data.get("retypePassword")
            print(changedPassword,retypePassword)
            #if the password matches the confirmation password, go through with the change
            if changedPassword == retypePassword:
                print("passwords equal")
                currAcc = User.objects.filter(username = request.user.username)
                #when the password is changed, log user out and direct them to the homepage
                for acc in currAcc:
                    acc.set_password(changedPassword)
                    acc.save()
                    print(acc.username, acc.password)
                    print("okay")
                    LoggingOut(request) 
                    return redirect('/pixelspace')
            else:
                print("passwords not the same")
        else:
            print("form invalid")
    else:
        print("nope")       
        form = changeForm()
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
        form=NameForm()

    #print(form)
    return render(request, 'pixelspace/create_account.html', {'form':form})
