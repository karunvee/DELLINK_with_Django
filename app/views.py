from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import *
from .tasks import urlDIA
# Create your views here.

def home_view(request):
    plant_members = PlantInfo.objects.all()
    

    dictLine = {}

    for plant in plant_members:
        url = urlDIA(plant.ip1, plant.port1, 'devices')
        line_members = requests.get(url).json()
        for line in line_members:
            #find @ in machine name
            if line['comment'].find('@') != -1:

                #split line name for machine name
                line_word = line['comment'].split("@")[0]
                machine_word = line['comment'].split("@")[1]
            else:
                line_word = "Unknown"
                machine_word = line['comment']

            #check key is not exist in dictionary
            if line_word in dictLine:
                dictLine[line_word].append(machine_word)
            else:   
                dictLine[line_word] = [machine_word]

    print(dictLine)
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