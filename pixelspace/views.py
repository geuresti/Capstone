from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
#from .models import Account
from django.contrib.auth.forms import UserCreationForm
from .forms import AccountForm
from .forms import NameForm
from .forms import LABForm
from .forms import createAccForm
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
            password= form.cleaned_data.get("password")

            print(user,password)
            return HttpResponseRedirect('/thanks/')
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

def createacc(request):
    template = loader.get_template('pixelspace/createacc.html')
    if request.method == 'POST':
        form = createAccForm(request.POST)
        if form.is_valid():
            print("in")
            newUser= form.cleaned_data.get("newUser")
            newPass= form.cleaned_data.get("newPass")
            confirmPass = form.cleaned_data.get("confirmPass")

            print(newUser,newPass, confirmPass)
            passwordValid = False
            if newPass == confirmPass:
                passwordValid = True
            print(passwordValid)
            return render(request, 'pixelspace/createacc.html', {'form':form, 'passwordValid' : passwordValid})
    else:
        print("NO")
        form=NameForm()

    #print(form)
    return render(request, 'pixelspace/createacc.html', {'form':form})

def testing(request):
    # If request = POST, create new user
    if request.method == 'POST':
    #    user_form = UserCreationForm(request.POST)
        user_form = AccountForm(request.POST)
        if user_form.is_valid():
            #print(type(request))
            print(request)
            print(request.body)
            data = json.loads(request.body)
            print(data)
            #print("STUFF 1:", request.read)
            #print("STUFF 2:", request.content_params)
        #    user_form.save()
            messages.success(request, 'Account successfully created.')

        #    new_acc = Account.objects.create(
        #                user=user,
        #                job_title=job_title
        #        )
            return redirect('test')
    # If request = GET, render a new account form
    else:
    #    user_form = UserCreationForm()
        user_form = AccountForm()
    page = 'pixelspace/createacc.html'
    return render(request, page, {'form':user_form})
