#!/usr/bin/python
          
import os  
import json
import sys        
import time
import serial
          
MY_SENDING_NODE_DEV0_PATH="/dev/ttyUSB0" 
MY_SENDING_NODE_DEV1_PATH="/dev/ttyUSB1" 

MY_SLEEP_INTERVAL=3
   
MY_MQTT_QUEUE_FILE_PATH="/var/lora_repeater/queue/"
MY_SENDING_FILE_PATH="/var/lora_repeater/sending/"
MY_SENT_FILE_PATH="/var/lora_repeater/sent/"
MY_SEND_FAIL_FILE_PATH="/var/lora_repeater/fail/"
MY_LOG_FILE_PATH="/var/lora_repeater/log/"


def check_lora_module(dev_path):
	try:
		ser = serial.Serial(dev_path, 9600, timeout=0.5)
		return ser
	except serial.serialutil.SerialException:
		#print 'FAIL: Cannot open Serial Port (No LoRa Node Inserted)'
		return None

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

ser = check_lora_module(MY_SENDING_NODE_DEV0_PATH)
if ser is None:
	ser = check_lora_module(MY_SENDING_NODE_DEV1_PATH)
	if ser is None:
		print 'FAIL to connect LoRa node!'
		sys.exit()
	else:
		print("Open LoRa node done:" + MY_SENDING_NODE_DEV1_PATH)   
else:   
	print("Open LoRa node done:" + MY_SENDING_NODE_DEV0_PATH)   


MY_NODE_MAC_ADDR=""
#queue my Lora node mac address AT+SGMD?, return +SGMD:"040004C5","GLN0161400362"
ser.write("AT+SGMD?\n")
return_state=ser.readlines()
#print return_state

matching = [s for s in return_state if "+SGMD:" in s]
#print matching  #['+SGMD:"05000095","GLN0154700000"\r\n']
MY_NODE_MAC_ADDR = "00000000"+matching[0][7:15]
print ("Check: My LoRa Node MAC Addr:" + MY_NODE_MAC_ADDR)

while 1:  
	for sending_f in os.listdir(MY_MQTT_QUEUE_FILE_PATH):
		print sending_f

		#read mqtt payload its mine
		if MY_NODE_MAC_ADDR in sending_f:
			print("#############Sending by Myself#########")
			os.remove(MY_MQTT_QUEUE_FILE_PATH+sending_f)
			continue
		else:
			print("Prepare to send data")
				
		os.rename(MY_MQTT_QUEUE_FILE_PATH+sending_f, MY_SENDING_FILE_PATH+sending_f)
		f = open(MY_SENDING_FILE_PATH+sending_f, 'r')
		f_json_data = f.read()
		f.close
		sensor_data = str(json.loads(f_json_data)[0]['data'])
		sensor_data_len = len(sensor_data)
		#print("sensor_data:" + sensor_data )
		data_sending = "AT+DTX="+str(sensor_data_len)+","+sensor_data+"\n"
		print(data_sending)
		#return_state=ser.readlines()
		#print(return_state)
		time.sleep(MY_SLEEP_INTERVAL)
		print('Sending')
		ser.write(data_sending)
		return_state=ser.readlines()
		print(return_state)
		if "OK\r\n" in return_state:
			print("Result: SENT.")
			os.rename(MY_SENDING_FILE_PATH+sending_f, MY_SENT_FILE_PATH+sending_f)
		else:
			print("Result: FAIL! move to FAIL")
			os.rename(MY_SENDING_FILE_PATH+sending_f, MY_SEND_FAIL_FILE_PATH+sending_f)
	else:
		print("Waiting for incoming queue")
		time.sleep(MY_SLEEP_INTERVAL)
ser.close
   

 