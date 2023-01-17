import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery import shared_task

from celery import Celery
from typing import Any, Dict
import msgpack
import json

from .models import *

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
def get_api():
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
        dictPlant["line"] = []
        machine_list = {}

        for url in urlLine:
            line_members = requests.get(url).json()
            for line in line_members:
                deviceNo = line['deviceId']
                status = line['status']
                deviceName = line['name']

                if line['comment'].find('@') != -1:
                    line_word = line['comment'].split("@")[0]
                    machine_word = line['comment'].split("@")[1]
                else:
                    line_word = "Unknown"
                    machine_word = line['comment']


                if line_word in machine_list:
                    machine_list[line_word].append([machine_word, deviceNo, status, deviceName, url])
                else:
                    machine_list[line_word] = [[machine_word, deviceNo, status, deviceName, url]]

        for key in machine_list.keys() :
            dictLine = {}
            dictLine["line_name"] = key
            dictLine["machine"] = []

            for mIndex in machine_list[key]:
                dictMachine = {}
                dictMachine["machine_name"] = mIndex[0]
                dictMachine["deviceId"] = mIndex[1]
                dictMachine["status"] = mIndex[2]
                dictMachine["device_name"] = mIndex[3]
                dictMachine["indicator"] = []

                indicator_members = requests.get(mIndex[4] + "/" + str(mIndex[1]) + "/tags").json()

                for indicator in indicator_members:
                    dictIndicator = {}
                    dictIndicator["indicator_name"] = indicator['name']
                    dictIndicator["tid"] = indicator['tid']
                    dictIndicator["register"] = indicator['register']
                    dictIndicator["gp"] = indicator['gp']
                    dictIndicator["value"] = str(indicator['value'])

                    dictMachine["indicator"].append(dictIndicator)
                
                dictLine["machine"].append(dictMachine)

                
            dictPlant["line"].append(dictLine)

        data.append(dictPlant)

    data_json = json.dumps(data)
    print("API fetching worker is listening..")
    publish_message_to_group({ "type": "chat_message", "text": data_json }, "app")

    # publish_message_to_group({ "type": "chat_message", "text": response }, "app")
    # response = requests.get(url).json()
    # msg = response['comment']

    # publish_message_to_group({ "type": "chat_message", "text": msg }, "app")
    # # async_to_sync(channel_layer.group_send)("app", {"type": "chat_message","text": msg,},)
    # print('<==================> message :' + msg)


#----------------------------------------
# import json
# from collections import defaultdict
# import requests
# import re

# def urlDIA(ip, port, method):
#     http_name = 'http://' + ip + ':' + port + '/api/v1/' + method
#     return http_name

# class plantlist:
# 	def __init__(self, name, ip1, port1, ip2="", port2="", ip3="", port3="", ip4="", port4=""):
# 		self.name = name
# 		self.ip1 = ip1
# 		self.port1 = port1
# 		self.ip2 = ip2
# 		self.port2 = port2
# 		self.ip3 = ip3
# 		self.port3 = port3
# 		self.ip4 = ip4
# 		self.port4 = port4

# plant1 = plantlist("DCBU", "10.195.220.7", "9000")
# plant2 = plantlist("CNBU", "10.195.220.30", "5000", "10.195.220.21" , "5000")
# plantList = [plant1, plant2]

# data = []
# urlLine = []
# machine_list = {}

# dictPlant = {}
# dictLine = {}
# dictMachine = {}
# dictIndicator = {}

# pattern = re.compile("[A-Za-z0-9]+")


# for plant in plantList:
# 	urlLine = []
# 	if plant.ip1 != "":
# 		urlLine.append(urlDIA(plant.ip1, plant.port1, 'devices')) 
# 	if plant.ip2 != "":
# 		urlLine.append(urlDIA(plant.ip2, plant.port2, 'devices'))   
# 	if plant.ip3 != "":
# 		urlLine.append(urlDIA(plant.ip3, plant.port3, 'devices'))  
# 	if plant.ip3 != "":
# 		urlLine.append(urlDIA(plant.ip4, plant.port4, 'devices')) 	 

# 	dictPlant = {}
# 	dictPlant["plant_name"] = plant.name
# 	dictPlant["line"] = []
# 	machine_list = {}

# 	for url in urlLine:
# 		line_members = requests.get(url).json()
# 		for line in line_members:
# 			deviceNo = line['deviceId']
# 			status = line['status']
# 			deviceName = line['name']

# 			if line['comment'].find('@') != -1:
# 				line_word = line['comment'].split("@")[0]
# 				machine_word = line['comment'].split("@")[1]
# 			else:
# 				line_word = "Unknown"
# 				machine_word = line['comment']


# 			if line_word in machine_list:
# 				machine_list[line_word].append([machine_word, deviceNo, status, deviceName, url])
# 			else:
# 				machine_list[line_word] = [[machine_word, deviceNo, status, deviceName, url]]

# 	for key in machine_list.keys() :
# 		dictLine = {}
# 		dictLine["line_name"] = key
# 		dictLine["machine"] = []

# 		for mIndex in machine_list[key]:
# 			dictMachine = {}
# 			dictMachine["machine_name"] = mIndex[0]
# 			dictMachine["deviceId"] = mIndex[1]
# 			dictMachine["status"] = mIndex[2]
# 			dictMachine["device_name"] = mIndex[3]
# 			dictMachine["indicator"] = []

# 			indicator_members = requests.get(mIndex[4] + "/" + str(mIndex[1]) + "/tags").json()

# 			for indicator in indicator_members:
# 				dictIndicator = {}
# 				dictIndicator["indicator_name"] = indicator['name']
# 				dictIndicator["tid"] = indicator['tid']
# 				dictIndicator["register"] = indicator['register']
# 				dictIndicator["gp"] = indicator['gp']
# 				dictIndicator["value"] = str(indicator['value'])

# 				#if pattern.fullmatch(str(indicator['value'])) is not None or str(indicator['value']) != None or str(indicator['value']) != "":
# 				#	dictIndicator["value"] = indicator['value']

# 				dictMachine["indicator"].append(dictIndicator)
			
# 			dictLine["machine"].append(dictMachine)

			
# 		dictPlant["line"].append(dictLine)

# 	data.append(dictPlant)

# print(data)
