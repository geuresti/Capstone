from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
#from .models import Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import AccountForm
from .forms import NameForm
from .forms import LABForm
from .forms import CreateAccountForm
from django.contrib import messages
from colormath.color_objects import LabColor, sRGBColor, AdobeRGBColor
from colormath.color_conversions import convert_color
import re
from colormath.color_diff import delta_e_cie1976

def index(request):
    template = loader.get_template('pixelspace/index.html')
    #return HttpResponse(template.render(request))
    latest_question_list = [1]
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def colors(request):
    template = loader.get_template('pixelspace/colors.html')
    if request.method == 'POST':
        form = LABForm(request.POST)
        if form.is_valid():
            print("in")
            lightness1 = form.cleaned_data.get("lightness")
            axisA = form.cleaned_data.get("axisA")
            axisB = form.cleaned_data.get("axisB")
            testing = [lightness1, axisA, axisB]
            print(lightness1,axisA,axisB)
            #return Response(testing)
            canRGB = False
            cansRGB = False
            lab = LabColor(lightness1, axisA, axisB)
            #print(lab)
            try:
                rgb = convert_color(lab, AdobeRGBColor)
                print(rgb)
                canRGB =  True
                hexCode = rgb.get_rgb_hex()
                #colors = [red,green,blue]
            except:
                canRGB = False
                hexCode = "#FFFFFF"
                rgb = "Not Applicable"

            try:
                srgb = convert_color(lab, sRGBColor)
                print(srgb)
                cansRGB =  True
                shexCode = srgb.get_rgb_hex()
                #colors = [red,green,blue]
            except:
                cansRGB = False
                shexCode = "#FFFFFF"
                srgb = "Not Applicable"

            shexCodeCheck = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', shexCode)
            if not shexCodeCheck:
                shexCode = "#FFFFFF"
                cansRGB = False

            hexCodeCheck = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hexCode)
            if not hexCodeCheck:
                hexCode = "#FFFFFF"
                canRGB = False

            return render(request, 'pixelspace/colors.html', {'form':form, 'canRGB': canRGB, 'hexCode': hexCode, 'rgb' : rgb, 'cansRGB': cansRGB, 'shexCode': shexCode, 'srgb' : srgb})

    else:
        print("NO")
        form=LABForm()

    #print(form)
    return render(request, 'pixelspace/colors.html', {'form':form})

def image(request):
    template = loader.get_template('pixelspace/image.html')
    #return HttpResponse(template.render(request))
    latest_question_list = [1]
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def login(request):
    template = loader.get_template('pixelspace/login.html')

    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            print("in")
            user= form.cleaned_data.get("username")
            password1= form.cleaned_data.get("password")
            accountValid = False
            print(user,password1)
            
            if User.objects.filter(username=user).exists():
                print("valid account")
                accountValid = True
                user123 = authenticate(username=user, password=password1)
                if user123:
                    return render(request, 'pixelspace/index.html', {'form':form, 'accountValid' : accountValid})
                else:
                    print("invalid account")

            else:
                print("invalid account")
            return render(request, 'pixelspace/login.html', {'form':form, 'accountValid' : accountValid})
    else:
        print("NO")
        form=NameForm()

    #print(form)
    return render(request, 'pixelspace/login.html', {'form':form})
    #return HttpResponse(template.render({'form':form}, request))

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

def settings(request):
    template = loader.get_template('pixelspace/settings.html')
    #return HttpResponse(template.render(request))
    latest_question_list = [1]
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def create_account(request):
    template = loader.get_template('pixelspace/create_account.html')
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():

            newUser= form.cleaned_data.get("newUser")
            newPass= form.cleaned_data.get("newPass")
            confirmPass = form.cleaned_data.get("confirmPass")

            # ! ERROR CHECK INPUT HERE !

            #print(newUser,newPass, confirmPass)
            passwordValid = False

            # If the input is valid, create a new user
            if newPass == confirmPass:
                passwordValid = True

                user = User.objects.create_user(
                    username=newUser,
                    password=newPass,
                #    email=email
                )
                #print(User.objects.all())
                
                #account = Account.objects.create(
                #        user=user
                #)
            else:
                print("Error: passwords did not match")
                # send error message
                #  to diff page

            return render(request, 'pixelspace/create_account.html', {'form':form, 'passwordValid' : passwordValid})
    else:
        print("NO")
        form=NameForm()

    #print(form)
    return render(request, 'pixelspace/create_account.html', {'form':form})
