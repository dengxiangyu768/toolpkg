#!/bin/bash


kubectl get configmap kube-proxy -n kube-system -o yaml > /tmp/kube-proxy.yml
local_ip={{ ansible_eth0.ipv4.address  }}
internal_slb_ip={{ apiserver_load_balance_ip }}
sed -i "/https/s/${local_ip}/${internal_slb_ip}/g" /tmp/kube-proxy.yml

kubectl replace -f /tmp/kube-proxy.yml

systemctl restart kubelet
systemctl enable kubelet
