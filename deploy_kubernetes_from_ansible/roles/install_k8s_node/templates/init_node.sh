#!/bin/bash

images=(
    pause-amd64:3.0
    kube-proxy-amd64:v1.6.1
    flannel:v0.8.0-amd64
    k8s-dns-sidecar-amd64:1.14.1
    k8s-dns-kube-dns-amd64:1.14.1
    k8s-dns-dnsmasq-nanny-amd64:1.14.1
)

for imageName in ${images[@]};do
  docker pull {{ harbor_domain }}/gcr.io/${imageName}
  docker tag docker.v2.aispeech.com/gcr.io/$imageName gcr.io/google_containers/$imageName
done


cd /tmp
wget {{ kubeadm_addr }}
wget {{ kubelet_addr }}
wget {{ kubectl_addr }}
wget {{ kubernetes_cni_addr }}

kubeadm_package_name=`echo {{ kubeadm_addr }}| awk -F '/' '{print $NF}'`
kubelet_package_name=`echo {{ kubelet_addr }}| awk -F '/' '{print $NF}'`
kubectl_package_name=`echo {{ kubectl_addr }}| awk -F '/' '{print $NF}'`
kubernetes_cni_package_name=`echo {{ kubernetes_cni_addr }}| awk -F '/' '{print $NF}'`

yum localinstall -y /tmp/{$kubeadm_package_name,$kubelet_package_name,$kubernetes_cni_package_name,$kubectl_package_name}

kubeadm join --token {{ kubernetes_token }} {{ master1_ip }}:6443
