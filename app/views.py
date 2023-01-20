from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from .models import *
from .tasks import urlDIA
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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
        'plant_name': pt,
        'line_name': ln,
    }
    return render(request, 'line_view.html', context)

def machine_view(request, pt, ln, mc):

    context = {

    }
    return render(request, 'machine_view.html', context)

@csrf_exempt
def SetLine(request, pt, ln):
    if request.method == 'POST':
        data_dictionary = json.loads(request.body.decode('utf-8'))

        print(data_dictionary)
        return JsonResponse({'status': 'success'})








    # else:
    #     return redirect('/line_view/pt{}ln{}/'.format(pt, ln))
    # if request.is_ajax():
    #     if request.method == 'POST':
    #         print('Raw Data: {}' .format(request.body)) 
    # data = json.loads(request.POST.get('data_dictionary'))
    # print(data)
    # data = request.POST['data_lineup']
    # print(data)
    # return redirect('/line_view/pt{}ln{}/'.format(pt, ln))
