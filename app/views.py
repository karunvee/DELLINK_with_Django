from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import *
from .tasks import urlDIA
import json

# Create your views here.

def home_view(request):
    plant_members = PlantInfo.objects.all()

    context = {
        'plant_members': plant_members,
    }
    # Return a response to the client
    return render(request, 'home_view.html', context)

def line_view(request, pt, ln):
    plant_members = PlantInfo.objects.all()

    context = {

    }
    return render(request, 'line_view.html', context)

def machine_view(request, pt, ln, mc):

    context = {

    }
    return render(request, 'machine_view.html', context)