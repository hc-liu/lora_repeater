#!/usr/bin/python

import paho.mqtt.client as mqtt
import json
import sys
import os 

MY_MQTT_QUEUE_FILE_PATH="/var/lora_repeater/queue/"
MY_SENDING_FILE_PATH="/var/lora_repeater/sending/"
MY_SENT_FILE_PATH="/var/lora_repeater/sent/"
MY_SEND_FAIL_FILE_PATH="/var/lora_repeater/fail/"
MY_LOG_FILE_PATH="/var/lora_repeater/log/"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")
    client.subscribe("#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    json_data = msg.payload
    sensor_mac = json.loads(json_data)[0]['macAddr']
    sensor_data = json.loads(json_data)[0]['data']
    sensor_count = json.loads(json_data)[0]['frameCnt']
    
    f = open(MY_MQTT_QUEUE_FILE_PATH+sensor_mac+"-"+str(sensor_count), 'w')
    f.write(json_data)
    f.close
    print('data = ' + sensor_data)
 
#start:    
#make queue file folder
if not os.path.exists(MY_MQTT_QUEUE_FILE_PATH):
    os.makedirs(MY_MQTT_QUEUE_FILE_PATH)
#make sending file folder    
if not os.path.exists(MY_SENDING_FILE_PATH):
    os.makedirs(MY_SENDING_FILE_PATH)
#make sent file folder    
if not os.path.exists(MY_SENT_FILE_PATH):
    os.makedirs(MY_SENT_FILE_PATH)
#make sending fail file folder    
if not os.path.exists(MY_SEND_FAIL_FILE_PATH):
    os.makedirs(MY_SEND_FAIL_FILE_PATH)            
#make log file folder
if not os.path.exists(MY_LOG_FILE_PATH):
    os.makedirs(MY_LOG_FILE_PATH)  
    
#clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp"
client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()