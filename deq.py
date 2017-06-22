#!/usr/bin/python
          
import os  
import json
import sys        
import time
import serial
          
MY_SENDING_NODE_DEV_PATH="/dev/ttyUSB0" 
MY_SLEEP_INTERVAL=3
   
MY_MQTT_QUEUE_FILE_PATH="/var/mqtt/queue"
MY_SENDING_FILE_PATH="/var/mqtt/sending"
MY_SENT_FILE_PATH="/var/mqtt/sent"
MY_SENT_FAIL_FILE_PATH="/var/mqtt/fail"

 
try:
    ser = serial.Serial(MY_SENDING_NODE_DEV_PATH, 9600, timeout=0.5)

except serial.serialutil.SerialException:
    print 'FAIL: Cannot open Serial Port (No LoRa Node Inserted)'
    sys.exit()
  
while 1:  
    for sending_f in os.listdir(MY_MQTT_QUEUE_FILE_PATH):
        print sending_f
        os.rename(MY_MQTT_QUEUE_FILE_PATH+"/"+sending_f, MY_SENDING_FILE_PATH+"/"+sending_f)
        f = open(MY_SENDING_FILE_PATH+"/"+sending_f, 'r')
        f_json_data = f.read()
        f.close
    
        sensor_data = str(json.loads(f_json_data)[0]['data'])
        sensor_data_len = len(sensor_data)
        #print("sensor_data:" + sensor_data )
        #print(len(sensor_data))
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
    		os.rename(MY_SENDING_FILE_PATH+"/"+sending_f, MY_SENT_FILE_PATH+"/"+sending_f)
    	else:
    		print("Result: FAIL! move to FAIL")
    		os.rename(MY_SENDING_FILE_PATH+"/"+sending_f, MY_SENT_FAIL_FILE_PATH+"/"+sending_f)
    
    print("Waiting for incoming queue"); time.sleep(MY_SLEEP_INTERVAL)

ser.close
   

 