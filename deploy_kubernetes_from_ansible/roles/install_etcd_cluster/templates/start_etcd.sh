#!/bin/bash

if [[ "{{ ansible_eth0.ipv4.address }}" == "{{ master1_ip }}" ]];then
  etcd_name="etcd0"
elif [[ "{{ ansible_eth0.ipv4.address }}" == "{{ master2_ip }}" ]];then
  etcd_name="etcd1"
else
  etcd_name="etcd2"
fi
docker run -d --net=host \
--restart always \
-v /data/resources/etcd-cluster:/var/lib/etcd \
-p 4001:4001 \
-p 2380:2380 \
-p 2379:2379 \
--name etcd \
gcr.io/google_containers/etcd-amd64:3.0.17 \
etcd --name=${etcd_name} \
--advertise-client-urls=http://{{ ansible_eth0.ipv4.address }}:2379,http://{{ ansible_eth0.ipv4.address }}:4001 \
--listen-client-urls=http://0.0.0.0:2379,http://0.0.0.0:4001 \
--initial-advertise-peer-urls=http://{{ ansible_eth0.ipv4.address }}:2380 \
--listen-peer-urls=http://0.0.0.0:2380 \
--initial-cluster-token=aispeech-etcd \
--initial-cluster=etcd0=http://{{ master1_ip }}:2380,etcd1=http://{{ master2_ip }}:2380,etcd2=http://{{ master3_ip }}:2380 \
--initial-cluster-state=new \
--data-dir=/var/lib/etcd
