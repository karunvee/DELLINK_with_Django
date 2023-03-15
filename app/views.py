from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.template import loader
import requests
from .forms import *
from .models import *
from .tasks import urlDIA
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

# Create your views here.
def remote_view(request):
    return render(request, 'remote_view.html', {})

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
    lineRow = LineRow.objects.filter(plant_name__exact = pt, line_name__exact = ln, name__exact = mc).get()

    if lineRow.remote_host != "" and lineRow.remote_host != "hostname":
        vnc_files_dir = os.path.join(os.path.dirname(__file__), 'static/js/nossh')
        jar_path = os.path.join(vnc_files_dir, 'tightvnc-jviewer.jar')
        # Launch the JAR file with the password argument
        hostname = lineRow.remote_host.split(':')
        host = hostname[0]
        port = hostname[1]
        password = lineRow.remote_password
        subprocess.Popen(['java', '-jar', jar_path,'-port={}'.format(port), '-host={}'.format(host) ,'-password={}'.format(password),
                        '-ViewOnly=no', '-ShowControls=no', '-showConnectionDialog=no'])

    
    notification_error = ErrorNotification.objects.filter(tag_member__line_name = ln, tag_member__machine_name = mc)
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
        'ip_camera' : lineRow.ip_camera,
        'indicator_members' : indicator_members,
        'machineInfo' : machineInfo,
        'form': form,
        'plantInfo': plantInfo,
        'lineName' : ln,
        'machineName': mc,
        'dia_url' : str_url,
        'ip_port' : ip_port,
        'notification_error' : notification_error,
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
        
            low_row.save()
        return JsonResponse({'status': 'success'})

def DeleteIndicator(request, pt, ln, mc, tid):
    indicator = Indicator.objects.get(plant_name__exact = pt, line_name__exact = ln, machine_name__exact = mc, tag_id__exact = tid)
    indicator.delete()
    return redirect('../../machine_view/pt{}ln{}mc{}/'.format(pt, ln, mc))

def DeleteData(request, pt, ln):

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



import subprocess
from mimetypes import guess_type
from websockify import WebSocketProxy


# def vnc_viewer(request, host, port, password):
#     vnc_files_dir = os.path.join(os.path.dirname(__file__), 'static/js/nossh')
#     jar_path = os.path.join(vnc_files_dir, 'tightvnc-jviewer.jar')
#     # Launch the JAR file with the password argument
#     subprocess.Popen(['java', '-jar', jar_path,'-port={}'.format(port), '-host={}'.format(host) ,'-password={}'.format(password),
#                        '-ViewOnly=no', '-ShowControls=no', '-showConnectionDialog=no'])
#     response = HttpResponse('VNC viewer is opening ...', {})
#     return redirect('home_view')

def vnc_viewer(request):
    try:
        print('vnc view')
        # process  = subprocess.Popen(['node', 'config.js'])
        # process.wait()
        # process.terminate()

        # # Open the file in read mode
        # with open('config.txt', 'r') as file:
        #     # Read the contents of the file
        #     file_contents = file.read()

        # print("###########\n{}\n###########".format(file_contents))

        # new_host = ",{target: '192.1681.102:5900', path: '/path3'}\n//"
        # # Modify the contents of the file
        # file_contents = file_contents.replace('//', new_host)

        # # Open the file in write mode
        # with open('config.txt', 'w') as file:
        #     # Write the modified contents back to the file
        #     file.write(file_contents)

        
    except:
        print("Can not found config.js on this directory path!")
    
    return render(request, 'vnc_view.html', {})