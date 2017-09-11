#!/bin/sh

echo "installing system required packages";
apt-get install -y mosquitto python-pip;
pip install --upgrade pip;
pip install paho-mqtt python-etcd pyserial PyMySql;

echo "installing lora_repeater package";
git clone https://github.com/hc-liu/lora_repeater.git;
cd lora_repeater/ ; 
cp inq.py deq.py /usr/local/bin/;
cp lora_repeater_starter /etc/init.d/;
chmod 755 /usr/local/bin/inq.py /usr/local/bin/deq.py /etc/init.d/lora_repeater_starter;
mv /usr/local/bin/inq.py /usr/local/bin/inq; mv /usr/local/bin/deq.py /usr/local/bin/deq;
update-rc.d lora_repeater_starter remove;
update-rc.d lora_repeater_starter defaults 99;

echo "Finished: lora_repeater_stater start or reboot wil be run";