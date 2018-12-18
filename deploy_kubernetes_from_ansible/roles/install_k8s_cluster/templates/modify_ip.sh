#!/bin/bash



#modify /etc/kubernetes/kubelet.conf
#modify /etc/kubernets/mani/kube-apiserver.conf

local_ip={{ ansible_eth0.ipv4.address }}
apiserver_config_ip=`cat /etc/kubernetes/manifests/kube-apiserver.yaml|grep advertise-address|cut -d '=' -f 2`

if [[ ${local_ip} == ${apiserver_config_ip} ]];then
  exit 0
else
  sed -i "/advertise-address/s/${apiserver_config_ip}/${local_ip}/g" /etc/kubernetes/manifests/kube-apiserver.yaml
  sed -i "/server/s/${apiserver_config_ip}/${local_ip}/g" /etc/kubernetes/kubelet.conf 
fi
