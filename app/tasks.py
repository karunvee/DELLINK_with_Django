import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery import shared_task

from celery import Celery
from typing import Any, Dict
import msgpack
import json

from .models import *
from datetime import datetime

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

@shared_task
def data_api():
    plant_members = PlantInfo.objects.all()
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
                    line_word = line['comment'].split("@")[0]
                    machine_word = line['comment'].split("@")[1]
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
                    error_code = "0"

                    dictMachine["indicator"].append(dictIndicator)

                    #Line notice error
                    
                    if(dictIndicator["indicator_name"] == "statusCode" and dictIndicator["value"] != "" and dictIndicator["value"] != "None" and (machine_name == "Auto load in router" or machine_name == "Auto Apply Glue") ):
                        if(dictIndicator["value"] != "0" and dictMachine["machine_name"] not in dicError):
                            errorNotice = ErrorNotification.objects.filter(
                                tag_member__plant_name__exact = dictPlant["plant_name"], 
                                tag_member__line_name__exact = dictLine["line_name"],
                                tag_member__machine_name__exact = dictMachine["machine_name"],
                                error_code__exact = dictIndicator["value"]
                            )
                            if(errorNotice.exists()):
                                msg_error = errorNotice.get()
                            else:
                                msg_error = "Error unknown, this error is not defined!"

                            dicError[dictMachine["machine_name"]] = dictIndicator["tid"]
                            
                            msg_alert = 'Error Alert\nmachine name:{}\nError code: ({}){}'.format(dictMachine["machine_name"], dictIndicator["value"], msg_error)
                            
                            # line_bot_api.broadcast(TextSendMessage(text=msg_alert))
                            # line_bot_api.broadcast(FlexSendMessage(alt_text="Card", contents=card))

                            #------------------------------------------------------------------------------------------------------------------------
                            # Add to Error history
                            now = datetime.now()
                            error_code = dictIndicator["value"]
                            errorAddCount = ErrorHistory(plant_name = dictPlant["plant_name"], line_name = dictLine["line_name"], machine_name = dictMachine["machine_name"]
                                                            , datetime = now, error_code = dictIndicator["value"], error_message = msg_error)
                            errorAddCount.save()
                            #------------------------------------------------------------------------------------------------------------------------
                        elif(dictIndicator["value"] == "0" and dictMachine["machine_name"] in dicError):
                            del dicError[dictMachine["machine_name"]]

                    # Timeline update
                    if(dictIndicator["indicator_name"] == "status" and dictIndicator["value"] != "" and dictIndicator["value"] != "None" and (machine_name == "Auto load in router" or machine_name == "Auto Apply Glue")):
                        timelineObj = TimeLineStatus.objects.filter(
                            plant_name__exact = dictPlant["plant_name"],
                            line_name__exact = dictLine["line_name"], 
                            machine_name__exact = dictMachine["machine_name"]
                        )

                        updateTimeline = False
                        if(dictIndicator["value"]  == "0"):
                            error_code = "0"
                            current_status = "Normal"
                        elif(dictIndicator["value"]  == "1"):
                            current_status = "Error"
                        else:
                            current_status = "Pause"

                        if(timelineObj.exists()):
                            old_value = timelineObj.order_by('-id')[0]
                            if(str(current_status) != str(old_value)):
                                updateTimeline = True
                                print("/{}<<current old>>>{}/".format(current_status, old_value))
                                print("Update status data")
                        else:
                            updateTimeline = True
                            print("Add new status data to database")

                        if(updateTimeline):
                                now = datetime.now()
                                # date = now.strftime("%Y-%m-%d")
                                # time = now.strftime("%H:%M:%S")

                                timeline = TimeLineStatus(plant_name = dictPlant["plant_name"], line_name = dictLine["line_name"], machine_name = dictMachine["machine_name"]
                                                        ,datetime = now, status = current_status, error_code = error_code)
                                timeline.save()
                                    
                                    

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


    data.append(dictType)
    # add day to datetime
    # oneDay = datetime.timedelta(days=1)

    # d1 = datetime.datetime(2020, 5, 13, 22, 50, 55) 
    # d2 = datetime.datetime(2020, 5, 13, 22, 50, 55)
    # d3 = datetime.datetime(2020, 6, 13, 7, 30, 0)

    # print(d1 > d2)
    # print(d2 > d3)
    
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

