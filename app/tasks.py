import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery import shared_task
import urllib.request
from celery import Celery
from typing import Any, Dict
import msgpack
import json

from .models import *
from datetime import datetime, timedelta
import pytz

from linebot.exceptions import InvalidSignatureError
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, AudienceRecipient, Filter, AgeFilter, Limit, RichMenu, RichMenuSize,
    RichMenuArea, RichMenuBounds, URIAction, FlexSendMessage, BubbleContainer, BoxComponent, TextComponent, SeparatorComponent
)
line_bot_api = LineBotApi('AGCpW+ldLVHm5eZKQ7Fm+Ph3mZZbjG9oAZU//pz7vzqH3UYSLQI8LRqPeLwuean6e39MpiC3RT/swpDUGHvDINfpH/ChLhWd0u/sEq+xwi0WC21a5xydQzMkplKB7Ata6D/VPiuLORmj4w4mN3KeYwdB04t89/1O/w1cDnyilFU=')

dicError = {}
channel_layer = get_channel_layer()

app = Celery('DELLINK')

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

def internet_on(http):
    try:
        urllib.request.urlopen(http, timeout=2)
        return True
    except:
        return False
    
def urlDIA(ip, port, method):
    http_name = 'http://' + ip + ':' + port + '/api/v1/' + method
    return http_name

def publish_message_to_group(message: Dict[str, Any], group: str) -> None:
    with app.producer_pool.acquire(block=True) as producer:
        producer.publish(
            msgpack.packb({
              "__asgi_group__": group,
              **message,
            }),
            exchange="groups",  # groups_exchange
            content_encoding="binary",
            routing_key=group,
            retry=False,  # Channel Layer at-most once semantics
        )
class machineStatus:
     def __init__(self, status, statusCode):
          self.status = status
          self.statusCode = statusCode

def MachineDashboard(machine_type, plant_name, line_name, machine_name, objStatus, errorKey):
    #Line notice error
    e_code = "0"
    if(objStatus.status != "" and objStatus.status != "None" and objStatus.statusCode != "" and objStatus.statusCode != "None"):
         
        if(objStatus.status == "1" and errorKey not in dicError):
            if(objStatus.statusCode != "0"):
                e_msg = ErrorMessage.objects.filter(
                    machine_type__machine_type__exact = machine_type,
                    error_code__exact = objStatus.statusCode
                )
                if(e_msg.exists()):
                    msg_error = e_msg.get()
                else:
                    msg_error = "Error unknown, this error is not defined!"

                dicError[errorKey] = objStatus.statusCode
                print("\n!!!!!!!! error >{} {}".format(errorKey, msg_error))
                
                msg_alert = 'Error Alert\nmachine name:{}\nError code: ({}){}'.format(machine_name, objStatus.statusCode, msg_error)
                
                # line_bot_api.broadcast(TextSendMessage(text=msg_alert))
                # line_bot_api.broadcast(FlexSendMessage(alt_text="Card", contents=card))

                #------------------------------------------------------------------------------------------------------------------------
                # Add to Error history
                now = datetime.now()
                errorAddCount = ErrorHistory(
                    plant_name = plant_name, 
                    line_name = line_name, 
                    machine_name = machine_name, 
                    datetime = now, 
                    error_code = objStatus.statusCode, 
                    error_message = msg_error)
                errorAddCount.save()
                #------------------------------------------------------------------------------------------------------------------------
        
        if(objStatus.status == "0" and objStatus.statusCode == "0" and errorKey in dicError):
            del dicError[errorKey]
    
        # Timeline update
        updateTimeline = False
        timelineObj = TimeLineStatus.objects.filter(
            plant_name__exact = plant_name,
            line_name__exact = line_name, 
            machine_name__exact = machine_name
        )
        # now = datetime.now(pytz.timezone('UTC'))
        now = datetime.now(pytz.timezone('Asia/Bangkok'))
        utilizationRateDay = UtilizationRatePerDay.objects.all()      
        #update datetime start - end
        datetimeStartEnd = TimeLineStartEnd.objects.all().order_by('-id')[0]
        if(datetimeStartEnd.end < now):
            # new_start = now.replace(hour=0, minute=30) #It's mean 7.30 am
            new_start = now.replace(hour=0, minute=0, second=0).astimezone(pytz.timezone('Asia/Bangkok'))
            new_end = new_start + timedelta(days = 1)  #Plus a day
            TimeLineStartEnd.objects.filter(pk = 2).update(start = new_start, end = new_end)
            print(" \n############## Update datetime start - end ##############\n{} {}".format(new_start, new_end))
            avg_utilization = 0
            if not utilizationRateDay.filter(exact__datetime = datetimeStartEnd.end).exists():
                timelineGreen = TimeLineStatus.objects.filter(
                    plant_name__exact = plant_name,
                    line_name__exact = line_name, 
                    machine_name__exact = machine_name,
                    status__exact = "Normal"
                )
                for item in timelineGreen:
                    item.datetime.timestamp() 
                # UtilizationRatePerDay(
                #     plant_name = plant_name, 
                #     line_name = line_name, 
                #     machine_name = machine_name, 
                #     datetime =  datetimeStartEnd.end, 
                #     rate = 90
                #     ).save()
                print(" \n<<<<<<<<<<<<<<< Add new Utilization Rate >>>>>>>>>>>>>>\n{}".format(datetimeStartEnd.end))
                        
        if(objStatus.status == "0"):
            current_status = "Normal"
        elif(objStatus.status == "1"):           
            current_status = "Error"
            if(errorKey in dicError):
                e_code = dicError[errorKey]
            else:
                e_code = "Is0"
        else:
            current_status = "Pause"
                   
        if(timelineObj.exists()):
            old_value = timelineObj.order_by('-id')[0]
            if(str(current_status) != str(old_value)):
                updateTimeline = True
                print("\n{} {} \nstatus has change from <{}> to <{}> <<errorCode: {}>>".format(line_name, machine_name, old_value, current_status, e_code))
            elif(old_value.datetime < datetimeStartEnd.start):
                print("Last status under datetime-start >> updated!\n{} {}".format(old_value.datetime, datetimeStartEnd.start))
                updateTimeline = True
        else:
            updateTimeline = True
            print("Add first status data to database")

        if(updateTimeline):
            TimeLineStatus(
                plant_name = plant_name, 
                line_name = line_name, 
                machine_name = machine_name,
                datetime = now, 
                status = current_status, 
                error_code = e_code
                ).save()

@shared_task
def data_api():
    plant_members = PlantInfo.objects.all()
    e_code = "0"
    data = []
    urlLine = []
    machine_list = {}

    dictPlant = {}
    dictLine = {}
    dictMachine = {}
    dictIndicator = {}

    for plant in plant_members:
        urlLine = []
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
        plant_name = plant.name
        dictPlant["line"] = []
        machine_list = {}

        for url in urlLine:
            if(internet_on(url)):
                line_members = requests.get(url).json()
                for line in line_members:
                    #get value of key from API 
                    deviceNo = line['deviceId']
                    status = line['status']
                    deviceName = line['name']
                    guid = line['guid']
                    type = line['type']
                    model = line['model']

                    if line['comment'].find('@') != -1:
                        try:
                            line_word = line['comment'].split("@")[0]
                            machine_word = line['comment'].split("@")[1]
                            machine_type = line['comment'].split("@")[2]
                        except Exception as e:
                            # print(e) 
                            machine_type = "No equipment type"
                    else:
                        line_word = "Unknown"
                        machine_word = line['comment']


                    if line_word in machine_list:
                        machine_list[line_word].append([url, machine_word, deviceNo, status, deviceName, guid, type, model])
                    else:
                        machine_list[line_word] = [[url, machine_word, deviceNo, status, deviceName, guid, type, model]]
                
        for key in machine_list.keys() :
            dictLine = {}
            dictLine["line_name"] = key
            line_name = key
            dictLine["machine"] = []

            for mIndex in machine_list[key]:

                status_dh = ""
                statusCode_dh = ""

                dictMachine = {}
                dictMachine["machine_name"] = mIndex[1]
                machine_name = mIndex[1]
                dictMachine["deviceId"] = mIndex[2]
                dictMachine["status"] = mIndex[3]
                dictMachine["device_name"] = mIndex[4]
                dictMachine["guid"] = mIndex[5]
                dictMachine["type"] = mIndex[6]
                dictMachine["model"] = mIndex[7]
                dictMachine["url"] = mIndex[0]
                dictMachine["indicator"] = []

                indicator_members = requests.get(mIndex[0] + "/" + str(mIndex[2]) + "/tags").json()
                for indicator in indicator_members:
                    dictIndicator = {}
                    dictIndicator["indicator_name"] = indicator['name']
                    dictIndicator["tid"] = indicator['tid']
                    dictIndicator["register"] = indicator['register']
                    dictIndicator["gp"] = indicator['gp']
                    dictIndicator["value"] = str(indicator['value'])
                    
                    if(dictIndicator["indicator_name"] == "status"):
                        status_dh = dictIndicator["value"]
                    elif(dictIndicator["indicator_name"] == "statusCode"):
                        statusCode_dh = dictIndicator["value"]

                    dictMachine["indicator"].append(dictIndicator)

                errorKey = "{}-{}".format(dictLine["line_name"], dictMachine["machine_name"])
                #Dashboard function here
                MachineDashboard(
                     machine_type, 
                     dictPlant["plant_name"], 
                     dictLine["line_name"], 
                     dictMachine["machine_name"], 
                     machineStatus(status_dh, statusCode_dh), 
                     errorKey
                     )
                

                dictLine["machine"].append(dictMachine)

                
            dictPlant["line"].append(dictLine)

        data.append(dictPlant)

    data_json = json.dumps(data)
    # print("API fetching worker is listening..")
    publish_message_to_group({ "type": "chat_message", "text": data_json }, "app")

@shared_task
def graph_api():
    data = []
    dictType = {}
    dictTimeline = {}
    dictError = {}


    timeline  = TimeLineStatus.objects.all()
    dictType["timeline"] = []
    for index in timeline:
        dictTimeline = {}
        dictTimeline["plant_name"] = index.plant_name
        dictTimeline["line_name"] = index.line_name
        dictTimeline["machine_name"] = index.machine_name
        dictTimeline["datetime"] = "{}".format(index.datetime)
        # dictTimeline["data_date"] = "{}".format(index.data_date)
        # dictTimeline["data_time"] = "{}".format(index.data_time)
        dictTimeline["status"] = index.status
        dictTimeline["error_code"] = index.error_code

        dictType["timeline"].append(dictTimeline)


    errorHistory = ErrorHistory.objects.all()
    dictType["error-history"] = []
    for index in errorHistory:
        dictError = {}
        dictError["plant_name"] = index.plant_name
        dictError["line_name"] = index.line_name
        dictError["machine_name"] = index.machine_name
        dictError["datetime"] = "{}".format(index.datetime)
        dictError["error_code"] = index.error_code
        dictError["error_message"] = index.error_message
        
        dictType["error-history"].append(dictError)

    dictType["utilization-rate"] = []
    

    data.append(dictType)
    
    data_json = json.dumps(data)
    # print(data_json)
    # print("Graph API fetching worker is listening..")
    publish_message_to_group({ "type": "chat_message", "text": data_json }, "graph")











    # publish_message_to_group({ "type": "chat_message", "text": response }, "app")
    # response = requests.get(url).json()
    # msg = response['comment']

    # publish_message_to_group({ "type": "chat_message", "text": msg }, "app")
    # # async_to_sync(channel_layer.group_send)("app", {"type": "chat_message","text": msg,},)
    # print('<==================> message :' + msg)
