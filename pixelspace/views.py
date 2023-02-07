from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("How are we lookin fellas")

# Create your views here.
