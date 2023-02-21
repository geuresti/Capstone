from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from .models import Account
from django.contrib.auth.forms import UserCreationForm
from .forms import AccountForm
from django.contrib import messages


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
    #return HttpResponse(template.render(request))
    latest_question_list = [1]
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

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
    #return HttpResponse(template.render(request))
    latest_question_list = [1]
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

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
