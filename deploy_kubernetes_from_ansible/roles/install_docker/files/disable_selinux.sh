#!/bin/bash

sed -i 's:SELINUX=enforcing:SELINUX=disabled:g' /etc/selinux/config
setenforce 0
sysctl -p /etc/sysctl.d/k8s.conf
exit 0
