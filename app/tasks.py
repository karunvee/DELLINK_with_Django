import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery import shared_task
from celery import Task, group
import urllib.request
from celery import Celery
from typing import Any, Dict
import msgpack
import json
from datetime import date 
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


def UtilizationRateHour(MACHINEDs):
    # PLANTs = PlantInfo.objects.get(name = "CNBU")
    # MACHINEDs = MachineMembers.objects.get(plantInfo = PLANTs, line_name = "CN05", machine_name = "Auto load in router")
    utilizationRate = 0
    now = datetime.now(pytz.timezone('Asia/Bangkok'))
    UtlPerHour = UtilizationRatePerHour.objects.filter(machineInfo = MACHINEDs, datetime__date = now)
    sum_greenTime = 0
    totalSecond = 0
    if UtlPerHour.exists():
        timeStart = now.replace(hour=len(UtlPerHour), minute=0, second=0).astimezone(pytz.timezone('Asia/Bangkok'))
    else:
        # first data
        timeStart = now.replace(hour=0, minute=0, second=0).astimezone(pytz.timezone('Asia/Bangkok'))

    if (now.timestamp() - timeStart.timestamp()) >= 3600 :

        nextHour = timeStart.replace(minute=0, second=0).astimezone(pytz.timezone('Asia/Bangkok')) + timedelta(hours=1)
        startHour = now.replace(hour=0, minute=0, second=0).astimezone(pytz.timezone('Asia/Bangkok'))

        timelineData = TimeLineStatus.objects.filter(
                machineInfo = MACHINEDs,
                datetime__date = now
        )
        if timelineData.exists():
            for i in range(0, len(timelineData), 1):
                try:
                        timeline_hourTime = timelineData[i].datetime.astimezone(pytz.timezone('Asia/Bangkok'))
                        
                        
                        if timelineData[i].status == "Normal" and  startHour < timeline_hourTime < nextHour:
                            if i == 0:
                                if timelineData[i+1].datetime.timestamp() > nextHour.timestamp():
                                    sum_greenTime = nextHour.timestamp() - timelineData[i].datetime.timestamp()
                                else:
                                    sum_greenTime = timelineData[i+1].datetime.timestamp() - timelineData[i].datetime.timestamp()
                            elif i == (len(timelineData) -1):
                                sum_greenTime = nextHour.timestamp() - timelineData[i].datetime.timestamp() + sum_greenTime
                            else:
                                sum_greenTime = timelineData[i+1].datetime.timestamp() - timelineData[i].datetime.timestamp() + sum_greenTime
 
                except:
                    break  
        totalSecond = nextHour.timestamp() - startHour.timestamp()          
        utilizationRate = (sum_greenTime*100) / totalSecond
        print("start :{} - now :{}  >>> {:.2f}% <s {}| t {}>".format(startHour, nextHour, utilizationRate, sum_greenTime, totalSecond))
        UtilizationRatePerHour(
            machineInfo = MACHINEDs, 
            datetime = nextHour,
            rate = abs(utilizationRate)
        ).save()

onCount = False
datetimeStart = datetime.now(pytz.timezone('Asia/Bangkok'))
datetimeEnd = datetime.now(pytz.timezone('Asia/Bangkok'))
datetimeTBS = datetime.now(pytz.timezone('Asia/Bangkok'))
tbs_rate = 0

@shared_task
def MachineDashboard(machine_type, plant_name, line_name, machine_name,  status_dh, statusCode_dh, errorKey):
    
    global onCount
    global tbs_rate
    global datetimeStart, datetimeEnd, datetimeTBS
    
    now = datetime.now(pytz.timezone('Asia/Bangkok'))
    objStatus = machineStatus(status_dh, statusCode_dh)

    PLANTs = PlantInfo.objects.get(name = plant_name)
    MACHINEDs = MachineMembers.objects.get(plantInfo = PLANTs, line_name = line_name, machine_name = machine_name)
    #Line notice error
    e_code = "0"
    # print("{} ******** {} <{}>".format(MACHINEDs, objStatus.status, objStatus.statusCode))
    if(objStatus.status != "" and objStatus.status != "None" and objStatus.statusCode != "" and objStatus.statusCode != "None"):
         
        if(objStatus.status == "1" and errorKey not in dicError):
            
            if(objStatus.statusCode != "0"):
                try:
                    ERROR_TYPEs = ErrorType.objects.filter(machine_type = machine_type)
                    if ERROR_TYPEs.exists():
                        error_type = ERROR_TYPEs.get()
                        MSG_ERRORs = ErrorMessage.objects.get(error_type = error_type, error_code__exact = objStatus.statusCode)
                    else:
                        UNDEFINED_TYPEs = ErrorType.objects.get(machine_type = "Undefined")
                        MSG_ERRORs = ErrorMessage.objects.get( error_type = UNDEFINED_TYPEs, error_code__exact = "NAN")
                except Exception as e:
                    print("Error at msg_error : {}".format(e))

                dicError[errorKey] = objStatus.statusCode


                print("\n!!!!!!!! error >{} {}".format(errorKey, MSG_ERRORs.error_message))
                
                # msg_alert = 'Error Alert\nmachine name:{}\nError code: ({}){}'.format(machine_name, objStatus.statusCode, MSG_ERRORs.error_message)
                
                # line_bot_api.broadcast(TextSendMessage(text=msg_alert))
                # line_bot_api.broadcast(FlexSendMessage(alt_text="Card", contents=card))

                #------------------------------------------------------------------------------------------------------------------------
                # Add to Error history
                # now = datetime.now(pytz.timezone('Asia/Bangkok'))
                errorAddCount = ErrorHistory(
                    machineInfo = MACHINEDs,
                    datetime = now, 
                    error_code = objStatus.statusCode, 
                    error_message = MSG_ERRORs)
                errorAddCount.save()
                #------------------------------------------------------------------------------------------------------------------------
        
        if(objStatus.status == "0" and objStatus.statusCode == "0" and errorKey in dicError):
            del dicError[errorKey]
    
    if(objStatus.status != "" and objStatus.status != "None"):
        # Timeline update  #------------------------------------------------------------------------------------------------------------------------
        updateTimeline = False
        timelineObj = TimeLineStatus.objects.filter(
            machineInfo = MACHINEDs
        )
        datetimeStartEnd = TimeLineStartEnd.objects.all().order_by('-id')[0]

        if(objStatus.status == "0"):
            current_status = "Normal"
            if not onCount and MACHINEDs.machine_name == "Auto load in router":
                onCount = True
                print("start TBS counting")

                tbs = TBS.objects.filter(machineInfo = MACHINEDs)
                if tbs.exists():
                    tbsObj = tbs.order_by('-id')[0]
                    print("datetimeTBS : {}".format(tbsObj.datetimeEnd))
                    datetimeTBS = tbsObj.datetimeEnd
                else:
                    datetimeTBS = datetime.now(pytz.timezone('Asia/Bangkok'))
                if tbs_rate != 0 :
                    datetimeEnd = datetime.now(pytz.timezone('Asia/Bangkok'))
                    duration = datetimeEnd.timestamp() - datetimeStart.timestamp()
                    print("\n\nTBS****[{}] {}\nstart {}\nend {}\nduration {}\nrate {}\n\n".format(
                        MACHINEDs.line_name, MACHINEDs.machine_name, 
                        datetimeStart, 
                        datetimeEnd, 
                        duration, tbs_rate))
                    TBS(machineInfo = MACHINEDs, 
                        datetimeStart = datetimeStart, 
                        datetimeEnd = datetimeEnd, 
                        duration = duration,
                        rate = tbs_rate).save()
                tbs_rate = 0
                
        elif(objStatus.status == "1"):           
            current_status = "Error"
            if(errorKey in dicError):
                e_code = dicError[errorKey]
            else:
                e_code = "Is0"
            
            if onCount and MACHINEDs.machine_name == "Auto load in router":
                onCount = False
                datetimeStart = datetime.now(pytz.timezone('Asia/Bangkok'))
                tbs_rate =  datetimeStart.timestamp() - datetimeTBS.timestamp()
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
            # print("Add first status data to database")

        if(updateTimeline):
            # now = datetime.now(pytz.timezone('Asia/Bangkok'))
            TimeLineStatus(
                machineInfo = MACHINEDs, 
                datetime = now, 
                status = current_status, 
                error_code = e_code
                ).save()
            
    #---- Utilization Rate----------------------------------------------------------------------------------------------------        
    # now = datetime.now(pytz.timezone('Asia/Bangkok'))     
        #update datetime start - end
    datetimeStartEnd = TimeLineStartEnd.objects.all().order_by('-id')[0]
        
    if(datetimeStartEnd.end < now):
        new_start = now.replace(hour=0, minute=0, second=0).astimezone(pytz.timezone('Asia/Bangkok'))
        new_end = new_start + timedelta(days = 1)  #Plus a day
        timeYesterday = new_start - timedelta(days = 1)
        sum_greenTime = 0
        DaySecond = 86400
        if not UtilizationRatePerDay.objects.filter(machineInfo = MACHINEDs, datetime__exact = timeYesterday.date()).exists():
            timelineData = TimeLineStatus.objects.filter(
                machineInfo = MACHINEDs,
                datetime__date = timeYesterday
            )
            if timelineData.exists():
                for i in range(0, len(timelineData), 1):
                    try:
                        if timelineData[i].status == "Normal":
                            if i == 0:
                                sum_greenTime = timelineData[i+1].datetime.timestamp() - timeYesterday.timestamp() + sum_greenTime
                            elif i == (len(timelineData) -1):
                                    sum_greenTime = new_start.timestamp() - timelineData[i].datetime.timestamp() + sum_greenTime
                            else:
                                sum_greenTime = timelineData[i+1].datetime.timestamp() - timelineData[i].datetime.timestamp() + sum_greenTime
                    except:
                        break                    

            utilizationRate = (sum_greenTime*100) / DaySecond
            print("{} - Utilization Rate : {}%".format(MACHINEDs, utilizationRate))
            UtilizationRatePerDay(
                machineInfo = MACHINEDs, 
                datetime =  timeYesterday, 
                rate = utilizationRate
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
        dataA = fetch_data_from_multiple_apis(urlLine)
        print(dataA)
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
                        status_dh = str(indicator['value'])
                    elif(dictIndicator["indicator_name"] == "statusCode"):
                        statusCode_dh = str(indicator['value'])
                    dictMachine["indicator"].append(dictIndicator)

                errorKey = "{}-{}".format(dictLine["line_name"], dictMachine["machine_name"])
                #Dashboard function here
                MachineDashboard.apply_async(
                    args=[
                        machine_type, 
                        dictPlant["plant_name"], 
                        dictLine["line_name"],
                        dictMachine["machine_name"], 
                        status_dh, statusCode_dh, 
                        errorKey])
                # MachineDashboard(
                #      machine_type, 
                #      dictPlant["plant_name"], 
                #      dictLine["line_name"], 
                #      dictMachine["machine_name"], 
                #      machineStatus(status_dh, statusCode_dh), 
                #      errorKey
                # )
                # UtilizationRateHour(
                #     machine_type, 
                #     dictPlant["plant_name"], 
                #     dictLine["line_name"], 
                #     dictMachine["machine_name"]
                # )

                dictLine["machine"].append(dictMachine)

                
            dictPlant["line"].append(dictLine)

        data.append(dictPlant)


    now = datetime.now(pytz.timezone('Asia/Bangkok'))    
    datetimeStartEnd = TimeLineStartEnd.objects.all().order_by('-id')[0]
    if(datetimeStartEnd.end < now):
        new_start = now.replace(hour=0, minute=0, second=0).astimezone(pytz.timezone('Asia/Bangkok'))
        new_end = new_start + timedelta(days = 1)  #Plus a day
        TimeLineStartEnd.objects.filter(pk = 2).update(start = new_start, end = new_end)
        print(" \n############## Update datetime start - end ##############\n{} {}".format(new_start, new_end))        

    # print("data api")
    data_json = json.dumps(data)
    publish_message_to_group({ "type": "chat_message", "text": data_json }, "app")
    
# @app.task
# def fetch_data_from_api(api_url):
#     data = requests.get(api_url).json()
#     return data

@app.task
def add(x, y):
    return {'result': x + y}

# def fetch_data_from_multiple_apis(api_urls):
#     # Use Celery group to execute tasks in parallel
#     # group_result = group(fetch_data_from_api.s(api_url) for api_url in api_urls)()
#     group_result = group(add.s(i, i) for i in range(2))()
#     # Get results from the group and return as a list of data
#     fetched_data = group_result.get(timeout=10)
#     return fetched_data

# @shared_task
# def function_fetching(machine_type, plant_name, line_name, machine_name, objectStatus, errorKey):
    # MachineDashboard(
    #                  machine_type, 
    #                  plant_name, 
    #                  line_name, 
    #                  machine_name, 
    #                  objectStatus, 
    #                  errorKey
    #             )

    # for plant in data:
    #     for line in plant['line']:
    #         line['line_name']
    #         if line['line_name'] == "D09A" :
    #             for machine in line['machine']:
    #                 status_dh = ""
    #                 statusCode_dh = ""
    #                 for indicator in machine['indicator']:
    #                     if indicator['indicator_name'] == 'status':
    #                         status_dh = str(indicator['value'])
    #                     elif indicator['indicator_name'] == 'statusCode':
    #                         statusCode_dh = str(indicator['value'])

    #                 print("function_fetching {}".format(machine['machine_name']))

@shared_task
def graph_api():
    data = []
    dictType = {}
    dictTimeline = {}
    dictError = {}
    now = datetime.now(pytz.timezone('Asia/Bangkok'))

    timeline  = TimeLineStatus.objects.filter(datetime__date = now)
    dictType["timeline"] = []
    for index in timeline:
        dictTimeline = {}
        dictTimeline["plant_name"] = index.machineInfo.plantInfo.name
        dictTimeline["line_name"] = index.machineInfo.line_name
        dictTimeline["machine_name"] = index.machineInfo.machine_name
        dictTimeline["datetime"] = "{}".format(index.datetime)
        dictTimeline["status"] = index.status
        dictTimeline["error_code"] = index.error_code

        dictType["timeline"].append(dictTimeline)


    errorHistory = ErrorHistory.objects.all()
    dictType["error-history"] = []
    for index in errorHistory:
        dictError = {}
        dictError["plant_name"] = index.machineInfo.plantInfo.name
        dictError["line_name"] = index.machineInfo.line_name
        dictError["machine_name"] = index.machineInfo.machine_name
        dictError["datetime"] = "{}".format(index.datetime)
        dictError["error_code"] = index.error_code
        dictError["error_message"] = index.error_message.error_message
        
        dictType["error-history"].append(dictError)

    UtilizationRate = UtilizationRatePerDay.objects.all()
    dictType["utilization-rate-day"] = []
    for index in UtilizationRate:
        dictUtilize = {}
        dictUtilize["plant_name"] = index.machineInfo.plantInfo.name
        dictUtilize["line_name"] = index.machineInfo.line_name
        dictUtilize["machine_name"] = index.machineInfo.machine_name
        dictUtilize["datetime"] = "{}".format(index.datetime)
        dictUtilize["rate-day"] = "{}".format(index.rate)
        dictType["utilization-rate-day"].append(dictUtilize)

    dictType["utilization-rate-hour"] = []
    
    MACHINEDs = MachineMembers.objects.all()
    for mIndex in MACHINEDs:
        UtilizationRateHour(mIndex)
        utl_hour = UtilizationRatePerHour.objects.filter(machineInfo = mIndex, datetime__date = now)
        dictUtlHour = {}
        dictUtlHour["plant_name"] = mIndex.plantInfo.name
        dictUtlHour["line_name"] = mIndex.line_name
        dictUtlHour["machine_name"] = mIndex.machine_name
        dictUtlHour["rate-hour"] = []
        for index in utl_hour:
            dicUtlData = {}
            dicUtlData["x"] = "{}".format(index.datetime)
            dicUtlData["y"] = "{}".format(index.rate)
            dictUtlHour["rate-hour"].append(dicUtlData)

        dictType["utilization-rate-hour"].append(dictUtlHour)
    data.append(dictType)
    

    data_json = json.dumps(data)
    publish_message_to_group({ "type": "chat_message", "text": data_json }, "graph")

@shared_task
def delete_expired_data():
    now = datetime.now(pytz.timezone('Asia/Bangkok'))
    ThreeDays_expired_date = now - timedelta(days = 3)
    threeMonths_expired_date = now - timedelta(days = 90)
    TwoYears_expired_date = now - timedelta(days = 730)

    # Expiration data is 3 Days 
    utilizationHour_expired = UtilizationRatePerHour.objects.filter(datetime__lte = TwoYears_expired_date)
    utilizationHour_expired.delete()
    timeline_expired = TimeLineStatus.objects.filter(datetime__lte = ThreeDays_expired_date)
    timeline_expired.delete()
    # Expiration data is 3 Months 

    # Expiration data is 2 Years 
    error_expired = ErrorHistory.objects.filter(datetime__lte = TwoYears_expired_date)
    error_expired.delete()
    utilizationDay_expired = UtilizationRatePerDay.objects.filter(datetime__lte = TwoYears_expired_date)
    utilizationDay_expired.delete()
