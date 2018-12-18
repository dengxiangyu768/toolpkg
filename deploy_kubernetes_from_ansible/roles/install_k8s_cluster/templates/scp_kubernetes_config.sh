#!/bin/bash

cat /etc/ssh/ssh_config|grep "StrictHostKeyChecking"|grep 'no'
result=$?
if [[ $result -eq 0 ]];then
   pass
else
   echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config
fi
if [[ "{{ ansible_eth0.ipv4.address }}" == "{{ master1_ip }}" ]];then
   scp -r /etc/kubernetes root@{{ master2_ip }}:/etc/
   scp -r /etc/kubernetes root@{{ master3_ip }}:/etc/
elif [[ "{{ ansible_eth0.ipv4.address }}" == "{{ master2_ip }}" ]];then
   scp -r /etc/kubernetes root@{{ master1_ip }}:/etc/
   scp -r /etc/kubernetes root@{{ master3_ip }}:/etc/
elif [[ "{{ ansible_eth0.ipv4.address }}" == "{{ master3_ip }}" ]];then
   scp -r  /etc/kubernetes root@{{ master1_ip }}:/etc/
   scp -r  /etc/kubernetes root@{{ master2_ip }}:/etc/
fi
