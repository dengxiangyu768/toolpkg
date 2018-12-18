#!/bin/bash
cd /tmp
wget {{ kubeadm_addr }}
wget {{ kubectl_addr }}
wget {{ kubelet_addr }}
wget {{ kubernetes_cni_addr }}

kubeadm_package_name=`echo {{ kubeadm_addr }}| awk -F '/' '{print $NF}'`
kubectl_package_name=`echo {{ kubectl_addr }}| awk -F '/' '{print $NF}'`
kubelet_package_name=`echo {{ kubelet_addr }}| awk -F '/' '{print $NF}'`
kubernetes_cni_package_name=`echo {{ kubernetes_cni_addr }}| awk -F '/' '{print $NF}'`

yum localinstall -y /tmp/{$kubeadm_package_name,$kubectl_package_name,$kubelet_package_name,$kubernetes_cni_package_name}
