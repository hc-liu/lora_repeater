#!/bin/sh

echo "installing system required packages";
sudo apt-get install -y mosquitto python-pip;
sudo pip install paho-mqtt python-etcd pyserial;

echo "installing lora_repeater package";
git clone https://github.com/hc-liu/lora_repeater.git
cd lora_repeater/ ; 
cp inq.py deq.py /usr/local/bin/;
sudo cp lora_repeater_starter /etc/init.d/;
sudo chmod 755 /usr/local/bin/inq.py /usr/local/bin/deq.py /etc/init.d/lora_repeater_starter;
mv /usr/local/bin/inq.py /usr/local/bin/inq; mv /usr/local/bin/deq.py /usr/local/bin/deq;
update-rc.d lora_repeater_starter remove;
update-rc.d lora_repeater_starter defaults;

echo "Finished: lora_repeater_stater start or reboot wil be run";