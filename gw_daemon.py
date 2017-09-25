#!/usr/bin/python

import time
import sys
import pprint
import uuid
import signal
import datetime
import paho.mqtt.client as mqtt
import json
import os

#pip install ibmiotf

try:
    import ibmiotf.application
    import ibmiotf.gateway
    from ibmiotf.codecs import jsonCodec, jsonIotfCodec
except ImportError:
    # This part is only required to run the sample from within the samples
    # directory when the module itself is not installed.
    #
    # If you have the module installed, just use "import ibmiotf.application" & "import ibmiotf.device"
    import os
    import inspect

    cmd_subfolder = os.path.realpath(
        os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../src")))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    import ibmiotf.application
    import ibmiotf.gateway

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # print("Connected with result code "+str(rc))
    print('Mqtt Connected.')
    client.subscribe("GIOT-GW/UL/")


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
        print(sensor_data)

        print('now frameCnt is:')
        print(sensor_count)

    except:
        print('Received a non-UTF8 msg')

def interruptHandler(signal, frame):
    gatewayCli.disconnect()
    sys.exit(0)

def myAppEventCallback(event):
    print("Received live data from %s (%s) sent at %s: hello=%s x=%s" % (
    event.deviceId, event.deviceType, event.timestamp.strftime("%H:%M:%S"), data['hello'], data['x']))


def myOnPublishCallback():
    print("Confirmed event %s received by IBM Watson IoT Platform\n" % x)

def get_mac():
  mac_num = hex(uuid.getnode()).replace('0x', '').upper()
  mac = '-'.join(mac_num[i : i + 2] for i in range(0, 11, 2))
  return mac

# start:
print('I am started!')
print get_mac()

organization = "l36bhs"
gatewayType = "Lora_gateway"
gatewayId = "00001c497bc0c083"

authMethod = "token"
authToken = "3JQKSZo@psD?EfJkvd"

# Initialize the device client.
try:
    gatewayOptions = {"org": organization, "type": gatewayType, "id": gatewayId, "auth-method": authMethod,
                      "auth-token": authToken}
    gatewayCli = ibmiotf.gateway.Client(gatewayOptions)
except Exception as e:
    print("Caught exception connecting device: %s" % str(e))
    sys.exit()

gatewayCli.connect()

# myData = '{"g":{"timestamp":"' + str(timestamp) + '","temperature":' + str(temperature) + "}}"
# print (myData)
# gatewayCli.setMessageEncoderModule('json', jsonCodec)
#
# gatewaySuccess = gatewayCli.publishGatewayEvent("greeting", "json", myData, qos=1, on_publish=myOnPublishCallback)
# deviceSuccess = gatewayCli.publishDeviceEvent("lora_node",
#                                                   "lora_node_device", "greeting", "json", myData,
#                                                   qos=1, on_publish=myOnPublishCallback)
# if not gatewaySuccess:
#     print("Gateway not connected to IBM Watson IoT Platform while publishing from Gateway")
#
# if not deviceSuccess:
#     print("Gateway not connected to IBM Watson IoT Platform while publishing from Gateway on behalf of a device")
#
# time.sleep(1)

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


# Disconnect the device and application from the cloud
#gatewayCli.disconnect()

