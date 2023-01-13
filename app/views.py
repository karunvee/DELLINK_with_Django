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
    
    urlLine = []
    data = []
    machine_list = {}

    dictPlant = {}
    dictLine = {}
    dictMachine = {}
    dictIndicator = {}
    
    for plant in plant_members:
        if plant.ip1 != "":
            urlLine.append(urlDIA(plant.ip1, plant.port1, 'devices')) 
        if plant.ip2 != "":
            urlLine.append(urlDIA(plant.ip2, plant.port2, 'devices'))   
        if plant.ip3 != "":
            urlLine.append(urlDIA(plant.ip3, plant.port3, 'devices'))  
        if plant.ip3 != "":
            urlLine.append(urlDIA(plant.ip4, plant.port4, 'devices'))   
        
        dictPlant = {}
        dictPlant["plant_name"] = plant.name
        dictPlant["line"] = []

        for urlIndex in urlLine:
            line_members = requests.get(urlIndex).json()
            for line in line_members:
                #find @ in machine name
                deviceNo = line['deviceId']

                if line['comment'].find('@') != -1:

                    #split line name for machine name
                    line_word = line['comment'].split("@")[0]
                    machine_word = line['comment'].split("@")[1]
                else:
                    line_word = "Unknown"
                    machine_word = line['comment']


                if line_word in dictLine:
                    machine_list[line_word].append({machine_word, deviceNo})
                else:   
                    machine_list[line_word] = [{machine_word, deviceNo}]

                # dictLine = {}
                # dictLine["line_name"] = line_word
                # dictLine["machine"] = []
                    


    #----------------------------------------------------------------------
    # dictPlant = {}
    # dictLine = {}
    # urlLine = []
    # for plant in plant_members:

    #     if plant.ip1 != "":
    #         urlLine.append(urlDIA(plant.ip1, plant.port1, 'devices')) 
    #     if plant.ip2 != "":
    #         urlLine.append(urlDIA(plant.ip2, plant.port2, 'devices'))   
    #     if plant.ip3 != "":
    #         urlLine.append(urlDIA(plant.ip3, plant.port3, 'devices'))  
    #     if plant.ip3 != "":
    #         urlLine.append(urlDIA(plant.ip4, plant.port4, 'devices'))   

    #     for urlIndex in urlLine:
    #         line_members = requests.get(urlIndex).json()
    #         for line in line_members:
    #             #find @ in machine name
    #             if line['comment'].find('@') != -1:

    #                 #split line name for machine name
    #                 line_word = line['comment'].split("@")[0]
    #                 machine_word = line['comment'].split("@")[1]
    #             else:
    #                 line_word = "Unknown"
    #                 machine_word = line['comment']

    #             #check key is not exist in dictionary
    #             if line_word in dictLine:
    #                 dictLine[line_word].append(machine_word)
    #             else:   
    #                 dictLine[line_word] = [machine_word]
    #   
    #     dictPlant[plant.name] = dictLine
    #     print(dictPlant)
    #     dictLine = {}
    #     urlLine = []
    #------------------------------------------------------------------------------
    # json_object = json.dumps(dictPlant, indent=4)
    # print(json_object)
    context = {
        'plant_members': plant_members,
        'dictPlant': dictPlant,
    }
    # Return a response to the client
    return render(request, 'home_view.html', context)

def line_view(request, pt, ln):
    plant_members = PlantInfo.objects.all()

    context = {

    }
    return render(request, 'line_view.html', context)