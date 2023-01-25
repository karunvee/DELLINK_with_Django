from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from .forms import *
from .models import *
from .tasks import urlDIA
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators import gzip

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
    line_row = LineRow.objects.filter(plant_name__exact = pt, line_name__exact = ln).order_by('number')
    context = {
        'plant_name': pt,
        'line_name': ln,
        'line_row' : line_row,
    }
    return render(request, 'line_view.html', context)

def machine_view(request, pt, ln, mc):
    if request.method == 'POST':
        form = LineRowForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = LineRowForm()

    machineInfo = LineRow.objects.filter(plant_name__exact = pt, line_name__exact = ln, name__exact = mc)
    context = {
        'machineInfo' : machineInfo.get(),
        'form': form,
    }

    return render(request, 'machine_view.html', context)

@csrf_exempt
def SetLine(request, pt, ln):

    if request.method == 'POST':
        
        data_dictionary = json.loads(request.body.decode('utf-8'))

        print(data_dictionary)
        LineRow.objects.filter(plant_name__exact = pt, line_name__exact = ln).delete()
        for i in range(1, len(data_dictionary) + 1, 1):
            low_row = LineRow(number = str(i), plant_name = pt, line_name = ln, deviceId = data_dictionary[str(i)][0], name = data_dictionary[str(i)][1], deviceName = data_dictionary[str(i)][2], status = data_dictionary[str(i)][3])
            print("number:{} plant:{} line:{} deviceId:{} name:{}".format(i, pt, ln, data_dictionary[str(i)][0], data_dictionary[str(i)][1]))
        
            low_row.save()
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
