#!/usr/bin/python
          
import os  
import json
import sys        
import time
import serial
import logging
from logging.handlers import RotatingFileHandler
          
MY_SENDING_NODE_DEV0_PATH="/dev/ttyUSB0" 
MY_SENDING_NODE_DEV1_PATH="/dev/ttyUSB1" 

MY_SLEEP_INTERVAL=3
MY_ALIVE_INTERVAL=60
   
MY_MQTT_QUEUE_FILE_PATH="/var/lora_repeater/queue/"
MY_SENDING_FILE_PATH="/var/lora_repeater/sending/"
MY_SENT_FILE_PATH="/var/lora_repeater/sent/"
MY_SEND_FAIL_FILE_PATH="/var/lora_repeater/fail/"
MY_LOG_FILE_PATH="/var/lora_repeater/log/"

MY_LOG_FILENAME = MY_LOG_FILE_PATH+"deq.log"

MY_NODE_MAC_ADDR=""
MY_NODE_MAC_ADDR_SHORT=""

GLOBAL_TIME_RUNNING=0
GLOBAL_COUNT_SENT=0
GLOBAL_COUNT_FAIL=0

def check_lora_module(dev_path):
	try:
		ser = serial.Serial(dev_path, 9600, timeout=0.5)
		return ser
	except serial.serialutil.SerialException:
		#print 'FAIL: Cannot open Serial Port (No LoRa Node Inserted)'
		return None

#start:   

# Set up a specific logger with our desired output level
my_logger = logging.getLogger('dequeue')
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
		#print 'FAIL to connect LoRa node!'
		my_logger.error('FAIL to connect LoRa node!')
		sys.exit()
	else:
		#print("Open LoRa node done:" + MY_SENDING_NODE_DEV1_PATH)   
		my_logger.info('Open LoRa node done: /dev/ttyUSB0')
else:   
	#print("Open LoRa node done:" + MY_SENDING_NODE_DEV0_PATH)  
	my_logger.info('Open LoRa node done: /dev/ttyUSB1')

#queue my Lora node mac address AT+SGMD?, return +SGMD:"040004C5","GLN0161400362"
ser.flushInput()
ser.flushOutput()
time.sleep(MY_SLEEP_INTERVAL)
ser.write("AT+SGMD?\n")
my_logger.info('Write AT+SGMD?')
return_state=ser.readlines()
#time.sleep(MY_SLEEP_INTERVAL)
#my_logger.info(return_state)
print return_state

if not return_state:
	my_logger.error('return of AT+SGMD? is empty!, restart!')
	ser.close
	time.sleep(MY_SLEEP_INTERVAL)
	os.execv(__file__, sys.argv)
else:
	my_logger.info(return_state)

matching = [s for s in return_state if "+SGMD:" in s]
#print matching  #['+SGMD:"05000095","GLN0154700000"\r\n']
MY_NODE_MAC_ADDR_SHORT = matching[0][7:15]
MY_NODE_MAC_ADDR = "00000000"+ MY_NODE_MAC_ADDR_SHORT
#print ("Check: My LoRa Node MAC Addr:" + MY_NODE_MAC_ADDR)
my_logger.info('Check: My LoRa Node MAC Addr:')
my_logger.info(MY_NODE_MAC_ADDR)


while 1:  
	for sending_f in os.listdir(MY_MQTT_QUEUE_FILE_PATH):
		#print sending_f
		my_logger.info(sending_f)
		#read mqtt payload its mine
		if MY_NODE_MAC_ADDR in sending_f:
			#print("#############Sending by Myself#########")
			my_logger.info('#############Sending by Myself#########')
			os.remove(MY_MQTT_QUEUE_FILE_PATH+sending_f)
			continue
		else:
			#print("Prepare to send data")
			my_logger.info('Prepare to send data')
				
		os.rename(MY_MQTT_QUEUE_FILE_PATH+sending_f, MY_SENDING_FILE_PATH+sending_f)
		f = open(MY_SENDING_FILE_PATH+sending_f, 'r')
		f_json_data = f.read()
		f.close
		sensor_data = str(json.loads(f_json_data)[0]['data'])
		sensor_data_len = len(sensor_data)
		#print("sensor_data:" + sensor_data )
		data_sending = "AT+DTX="+str(sensor_data_len)+","+sensor_data+"\n"
		time.sleep(MY_SLEEP_INTERVAL)
		GLOBAL_TIME_RUNNING+=MY_SLEEP_INTERVAL
		#print('Sending')
		my_logger.info('Sending')
		ser.flushInput()
		ser.flushOutput()
		ser.write(data_sending)
		my_logger.info(data_sending)
		return_state=ser.readlines()
		#print(return_state)
		my_logger.info(return_state)
		if "OK\r\n" in return_state:
			#print("Result: SENT.")
			my_logger.info('Result: SENT.')
			GLOBAL_COUNT_SENT+=1
			os.rename(MY_SENDING_FILE_PATH+sending_f, MY_SENT_FILE_PATH+sending_f)
		else:
			#print("Result: FAIL! move to FAIL")
			my_logger.error('Result: FAIL! move to FAIL.')
			GLOBAL_COUNT_FAIL+=1
			os.rename(MY_SENDING_FILE_PATH+sending_f, MY_SEND_FAIL_FILE_PATH+sending_f)
	else:
		#print("Waiting for incoming queue")
		time.sleep(MY_SLEEP_INTERVAL)
		GLOBAL_TIME_RUNNING+=MY_SLEEP_INTERVAL
	
	#print("in while loop")
	if GLOBAL_TIME_RUNNING >= MY_ALIVE_INTERVAL:
		#send alive command
		time.sleep(MY_SLEEP_INTERVAL)
		data_alive = MY_NODE_MAC_ADDR_SHORT + "E" +str(GLOBAL_COUNT_SENT) + "F" +str(GLOBAL_COUNT_FAIL)
		data_alive_send = "AT+DTX=" + str (len(data_alive)) + "," + data_alive + "\n"
		ser.flushInput()
		ser.flushOutput()
		my_logger.info(data_alive_send)
		ser.write(data_alive_send)
		return_state=ser.readlines()
		my_logger.info('Alive message')
		my_logger.info(return_state)
		#print(return_state)
		GLOBAL_COUNT_SENT=0
		GLOBAL_COUNT_FAIL=0
		GLOBAL_TIME_RUNNING=0
ser.close
   

 