#!/bin/bash

sleep 10

echo "export KUBECONFIG=/etc/kubernetes/admin.conf" >> ~/.bash_profile

source ~/.bash_profile

kubectl create -f /tmp/flannel.yaml
