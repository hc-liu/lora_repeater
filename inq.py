#!/usr/bin/python

import paho.mqtt.client as mqtt
import json
import sys

MY_SENDING_NODE="0000000005000095"

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
    
    if sensor_mac == MY_SENDING_NODE:
        print("#############Sending by Myself#########")
    else:
    	f = open("/var/mqtt/queue/"+sensor_mac+"-"+str(sensor_count), 'w')
    	f.write(json_data)
    	f.close
    	print('data = ' + sensor_data)
    


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