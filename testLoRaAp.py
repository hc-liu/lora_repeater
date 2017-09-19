#!/usr/bin/python

import paho.mqtt.client as mqtt
import json
import sys
import os

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # print("Connected with result code "+str(rc))
    print('Mqtt Connected.')
    client.subscribe("#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        # print(msg.topic+" "+str(msg.payload))
        print('Message incoming')
        print(msg.topic)
        print(msg.payload)
        json_data = msg.payload
        sensor_mac = json.loads(json_data)[0]['macAddr']
        sensor_data = json.loads(json_data)[0]['data']
        sensor_count = json.loads(json_data)[0]['frameCnt']
        nFrameCnt = json.loads(json_data)[0]['frameCnt']

        print('Data is:')
        print(sensor_data)

        print('now frameCnt is:')
        print(sensor_count)

    except:
        print('Received a non-UTF8 msg')


# start:
print('I am started!')

# clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp"
client = mqtt.Client(protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
