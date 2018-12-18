#!/bin/bash



images=(
    pause-amd64:3.0
    kube-proxy-amd64:v1.6.1
    kube-scheduler-amd64:v1.6.1
    kube-controller-manager-amd64:v1.6.1
    kube-apiserver-amd64:v1.6.1
    etcd-amd64:3.0.17
    flannel:v0.8.0-amd64
    k8s-dns-sidecar-amd64:1.14.1
    k8s-dns-kube-dns-amd64:1.14.1
    k8s-dns-dnsmasq-nanny-amd64:1.14.1
)

for imageName in ${images[@]};do
  docker pull {{ harbor_domain }}/gcr.io/${imageName}
  docker tag docker.v2.aispeech.com/gcr.io/$imageName gcr.io/google_containers/$imageName
done
