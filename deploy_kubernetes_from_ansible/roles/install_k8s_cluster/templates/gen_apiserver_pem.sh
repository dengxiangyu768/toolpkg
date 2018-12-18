#!/bin/bash
#date:2018-4-25



mkdir -p /etc/kubernetes/pki-local
cd /etc/kubernetes/pki-local
openssl genrsa -out apiserver.key 2048
openssl req -new -key apiserver.key -subj "/CN=kube-apiserver," -out apiserver.csr

echo "subjectAltName = DNS:`hostname`,DNS:kubernetes,DNS:kubernetes.default,DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster.local, IP:10.96.0.1, IP:{{ ansible_eth0.ipv4.address }},IP:{{ apiserver_load_balance_ip }}" > apiserver.ext
openssl x509 -req -in apiserver.csr -CA /etc/kubernetes/pki/ca.crt -CAkey /etc/kubernetes/pki/ca.key -CAcreateserial -out apiserver.crt -days 365 -extfile /etc/kubernetes/pki-local/apiserver.ext
cp -f apiserver.crt apiserver.key /etc/kubernetes/pki/


systemctl daemon-reload && systemctl restart docker kubelet


