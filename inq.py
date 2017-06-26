#!/usr/bin/python

import paho.mqtt.client as mqtt
import json
import sys
import os 
import logging
from logging.handlers import RotatingFileHandler

MY_MQTT_QUEUE_FILE_PATH="/var/lora_repeater/queue/"
MY_SENDING_FILE_PATH="/var/lora_repeater/sending/"
MY_SENT_FILE_PATH="/var/lora_repeater/sent/"
MY_SEND_FAIL_FILE_PATH="/var/lora_repeater/fail/"
MY_LOG_FILE_PATH="/var/lora_repeater/log/"

MY_LOG_FILENAME = MY_LOG_FILE_PATH+"inq.log"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))
	my_logger.info('Mqtt Connected.')
	client.subscribe("#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
    	#print(msg.topic+" "+str(msg.payload))
    	my_logger.info('Message incoming')
    	my_logger.info(msg.topic)
    	my_logger.info(msg.payload) 
    	json_data = msg.payload
    	sensor_mac = json.loads(json_data)[0]['macAddr']
    	sensor_data = json.loads(json_data)[0]['data']
    	sensor_count = json.loads(json_data)[0]['frameCnt']
    
    	my_logger.info('Data is:')
    	my_logger.info(sensor_data)
    	f = open(MY_MQTT_QUEUE_FILE_PATH+sensor_mac+"-"+str(sensor_count), 'w')
    	f.write(json_data)
    	f.close
    	#print('data = ' + sensor_data)
    except:
    	my_logger.error('Received a non-UTF8 msg')
 
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

# Set up a specific logger with our desired output level
my_logger = logging.getLogger('enqueue')
# Add the log message handler to the logger
my_logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(MY_LOG_FILENAME, maxBytes=10240, backupCount=100)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
my_logger.addHandler(handler)
my_logger.info('I am started!')
#example
#my_logger.debug('debug message')
#my_logger.info('info message')
#my_logger.warn('warn message')
#my_logger.error('error message')
#my_logger.critical('critical message')
 
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