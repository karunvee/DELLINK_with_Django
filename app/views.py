from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.template import loader
import requests
from .forms import *
from .models import *
from .tasks import urlDIA, add
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import cv2
import threading
import urllib.request
from django.views.decorators import gzip
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save
import os
from vncdotool import client, rfb, api
import base64
import subprocess
from mimetypes import guess_type
from websockify import WebSocketProxy
from datetime import datetime, timedelta
import pytz
from django.contrib.auth.decorators import login_required


# Create your views here.
def remote_view(request):
    return render(request, 'remote_view.html', {})

def home_view(request):
    plant_members = PlantInfo.objects.all()
    val = add.delay(2,2)
    print(val['result'])
    context = {
        'add' : val,
        'plant_members': plant_members,
    }
    # Return a response to the client
    return render(request, 'home_view.html', context)

@login_required
def line_view(request, pt, ln):
    # PLANTs = PlantInfo.objects.get(name = pt)
    line_row = LineRow.objects.filter(plant_name__exact = pt, line_name__exact = ln).order_by('number')
    context = {
        'plant_name': pt,
        'line_name': ln,
        'line_row' : line_row,
    }
    return render(request, 'line_view.html', context)

@login_required
def machine_view(request, pt, ln, mc):
    
    indicator_members = Indicator.objects.filter(plant_name__exact = pt, line_name__exact = ln, machine_name__exact = mc)
    plantInfo = PlantInfo.objects.filter(name__exact = pt).get()

    old_img = LineRow.objects.filter(plant_name__exact = pt, line_name__exact = ln, name__exact = mc).get()
    if request.method == 'POST':
        form = LineRowForm(request.POST or None, request.FILES or None, instance=old_img)
        if form.is_valid():
            # deleting old uploaded image.
            form.save()
            # return redirect('success')
            return redirect('../../machine_view/pt{}ln{}mc{}/'.format(pt, ln, mc))
    else:
        form = LineRowForm(instance=old_img)

    machineInfo = LineRow.objects.filter(plant_name__exact = pt, line_name__exact = ln, name__exact = mc).get()
    url = machineInfo.url.split('api')
    str_url = '{}devices/{}/{}/tags'.format(url[0], machineInfo.guid, machineInfo.deviceId)
    ip_port = url[0]

    context = {
        'machine_view': True,
        'indicator_members' : indicator_members,
        'machineInfo' : machineInfo,
        'form': form,
        'plantInfo': plantInfo,
        'lineName' : ln,
        'machineName': mc,
        'dia_url' : str_url,
        'ip_port' : ip_port,
        'errData_count' : [30, 49, 44, 24, 15],
    }
    return render(request, 'machine_view.html', context)


@receiver(pre_save, sender=LineRow)
def delete_old_file(sender, instance, **kwargs):
    try:
        old_file = sender.objects.get(pk=instance.pk).picturePath
    except sender.DoesNotExist:
        return
    new_file = instance.picturePath
    if not old_file == new_file:
        # if os.path.isfile(old_file.path):
        if old_file and hasattr(old_file, 'path') and os.path.isfile(old_file.path):
            os.remove(old_file.path)

@csrf_exempt
def SetLine(request, pt, ln):

    if request.method == 'POST':
        
        data_dictionary = json.loads(request.body.decode('utf-8'))
        plant = PlantInfo.objects.get(name = pt)
        print(data_dictionary)
        LineRow.objects.filter(plant_name__exact = pt, line_name__exact = ln).delete()
        for i in range(1, len(data_dictionary) + 1, 1):
            low_row = LineRow(
                number = str(i), 
                plant_name = pt, 
                line_name = ln, 
                deviceId = data_dictionary[str(i)][0], 
                name = data_dictionary[str(i)][1], 
                deviceName = data_dictionary[str(i)][2], 
                status = data_dictionary[str(i)][3],
                type = data_dictionary[str(i)][4],
                model = data_dictionary[str(i)][5],
                guid = data_dictionary[str(i)][6],
                url = data_dictionary[str(i)][7],
                )
            print("number:{} plant:{} line:{} deviceId:{} name:{}".format(i, pt, ln, data_dictionary[str(i)][0], data_dictionary[str(i)][1]))
            
            
            MachineMembers(
                plantInfo = plant,
                line_name = ln,
                machine_name = data_dictionary[str(i)][1]
            ).save()
            low_row.save()
        return JsonResponse({'status': 'success'})

def DeleteIndicator(request, pt, ln, mc, tid):
    indicator = Indicator.objects.get(plant_name__exact = pt, line_name__exact = ln, machine_name__exact = mc, tag_id__exact = tid)
    indicator.delete()
    return redirect('../../machine_view/pt{}ln{}mc{}/'.format(pt, ln, mc))

def DeleteData(request, pt, ln):
    plant = PlantInfo.objects.get(name = pt)
    MachineMembers.objects.filter(plantInfo = plant,line_name = ln).delete()
    LineRow.objects.filter(plant_name__exact = pt, line_name__exact = ln).delete()

    return redirect('../../line_view/pt{}ln{}/'.format(pt, ln))

def AssignIndicator(request, pt, ln, mc):

    if request.method == 'POST':
        tag_name = request.POST['tagName']
        tag_id = request.POST['tagID']
        register = request.POST['register']
        data_type = request.POST['data_type']
        if data_type == 'BIT':
            display = request.POST['display_type_bit']
        else:
            display = request.POST['display_type_text']
        color = request.POST['color']
        indicator_members = Indicator(plant_name = pt, line_name = ln, machine_name = mc, tag_name = tag_name, tag_id = tag_id, register = register, data_type = data_type, display = display, color = color)
        indicator_members.save()
        return redirect('../../machine_view/pt{}ln{}mc{}/'.format(pt, ln, mc))

def AssignCamera(request, pt, ln, mc):
    if request.method == 'POST':
        LineRow.objects.filter(plant_name__exact = pt, line_name__exact = ln, name__exact = mc).update(ip_camera = request.POST['ip_camera'])
        return redirect('../../machine_view/pt{}ln{}mc{}/'.format(pt, ln, mc))

    
def internet_on(http):
    try:
        urllib.request.urlopen(http, timeout=2)
        return True
    except:
        return False

@gzip.gzip_page
def camera_view(request, pt, ln, mc):
    if(LineRow.objects.filter(plant_name__exact = pt, line_name__exact = ln, name__exact = mc).exists()):
        machineData = LineRow.objects.filter(plant_name__exact = pt, line_name__exact = ln, name__exact = mc).get()
        print("%s Data of camera exist! line: %s machine: %s >>> %s" % (request, ln, mc, machineData.ip_camera))
        if internet_on("http://%s" % ( machineData.ip_camera)) == False:
            print("IP: %s is not connected the camera" %  machineData.ip_camera)
            return render(request, 'camera_view.html')
        else:
            print("IP: %s is connected!" %  machineData.ip_camera)
    else:
        print("%s Data of camera doesn't exist! line: %s id: %s" % (request, ln, mc))
        return render(request, 'camera_view.html', {'data_exist' : "False"})
    
    try:
        rtsp = "rtsp://admin:admin123@"+ str( machineData.ip_camera) + "/cam/realmonitor?channel=1&subtype=00"
        cam = VideoCamera(rtsp)
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'camera_view.html')
#to capture video class
class VideoCamera(object):
    def __init__(self, rtsp):
        self.video = cv2.VideoCapture(rtsp)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        try:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except:
            print("Can not found the response form this rtsp.")
            break

#Run Node config.js after start the server ---------------
#.
js_file = "./Config.js"
# node_process  = subprocess.Popen(['node', js_file])  <<< Open Websockify here
#---------------------------------------------------------
def restart_process(process, command):
    global node_process
    process.terminate()
    process.wait()
    node_process = subprocess.Popen(command)
    return node_process

def updateConfig(request, pt, ln, mc):
    
    if request.method == 'POST':
        LineRow.objects.filter(plant_name__exact = pt, line_name__exact = ln, name__exact = mc).update(remote_host = request.POST['remote_host'], remote_password = request.POST['remote_password'])

    line_row = LineRow.objects.all()
    path_txt = """"""
    for item in line_row:
        if(item.remote_host != "hostname"):
            path_txt += "{target: '"+item.remote_host+"', path: '/"+ item.deviceName +"'},"
    try:
        if os.path.exists(js_file):
            os.remove(js_file)

        context = """
            const http = require('http')
            const port = process.env.PORT || 8086
            const websockify = require('@sukkis/node-multi-websockify')
            const server = http.createServer()
            server.listen(port)
            websockify(server, 
            [
                {}
                ])""".format(path_txt)

        with open(js_file, 'a') as file:
            file.write(context.strip())

        # global node_process
        # node_process = restart_process( node_process, ['node', js_file])


        print("***  Node is running with new config.js  ***")
    
        return redirect('../../machine_view/pt{}ln{}mc{}/'.format(pt, ln, mc))
    except Exception as e:
        return HttpResponse(e)
    

def vnc_viewer(request):
    try:
        print('vnc view')
        
    except:
        print("Can not found config.js on this directory path!")
    
    return render(request, 'vnc_view.html', {})

def DeleteErrorHistory(request):
    ErrorHistory.objects.all().delete()
    return HttpResponse("Delete all error history success!")

def DeleteTimeline(request):
    TimeLineStatus.objects.all().delete()
    return HttpResponse("Delete all timeline success!")

def DeleteUtilizationDays(request):
    UtilizationRatePerDay.objects.all().delete()
    return HttpResponse("Delete all Utilization Days success!")

def DeleteUtilizationHours(request):
    UtilizationRatePerHour.objects.all().delete()
    return HttpResponse("Delete all Utilization Hours success!")

def updatetimestart(request):
    now = datetime.now(pytz.timezone('Asia/Bangkok'))
    new_start = now.replace(hour=0, minute=0, second=0).astimezone(pytz.timezone('Asia/Bangkok')) #It's mean 7.30 am
    new_end = new_start + timedelta(days = 1)  #Plus a day
    TimeLineStartEnd.objects.filter(pk = 2).update(start = new_start, end = new_end)

    return HttpResponse("Datetime updated!")