#!/bin/bash

domain={{ harbor_domain }}
ip={{ harbor_addr }}
cat /etc/hosts|grep ${domain}|grep ${ip}
result=$?
if [[ $result -ne 0 ]];then
  echo ${ip} ${domain} >> /etc/hosts  
fi
