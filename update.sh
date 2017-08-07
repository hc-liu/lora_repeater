#!/bin/sh

git fetch;
git pull origin master:master;
cp inq.py deq.py /usr/local/bin/;
cp lora_repeater_starter /etc/init.d/;
chmod 755 /usr/local/bin/inq.py /usr/local/bin/deq.py /etc/init.d/lora_repeater_starter;
mv /usr/local/bin/inq.py /usr/local/bin/inq; mv /usr/local/bin/deq.py /usr/local/bin/deq;
update-rc.d lora_repeater_starter remove;
update-rc.d lora_repeater_starter defaults;

echo "Finished: lora_repeater_stater start or reboot wil be run";
