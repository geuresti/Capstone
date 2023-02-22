from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
#from .models import Account
from django.contrib.auth.forms import UserCreationForm
from .forms import AccountForm
from .forms import NameForm
from .forms import LABForm
from django.contrib import messages
from colormath.color_objects import LabColor, sRGBColor, AdobeRGBColor
from colormath.color_conversions import convert_color


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
                hexCode = "Not Applicable"


            return render(request, 'pixelspace/colors.html', {'form':form, 'canRGB': canRGB, 'hexCode': hexCode})
           
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
    #return HttpResponse(template.render(request))
    latest_question_list = [1]
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

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
