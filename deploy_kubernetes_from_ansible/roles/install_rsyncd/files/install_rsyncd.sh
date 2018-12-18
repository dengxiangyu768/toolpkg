#!/bin/bash
#date: 2017-11-23

cat <<\EOF > /etc/rsyncd.conf
#Minimal configuration file for rsync daemon
# See rsync(1) and rsyncd.conf(5) man pages for help
#
# This line is required by the /etc/init.d/rsyncd script
#
pid file = /var/run/rsyncd.pid
#address = 172.16.10.19
address = 0.0.0.0
port = 873

#uid = nobody
#gid = nobody   
uid = root
gid = root

use chroot = yes
read only = yes


#limit access to private LANs
hosts allow = *
#hosts deny = *

#This will give you a separate log file
log file = /var/log/rsync.log

#This will log every file transferred - up to 85,000+ per user, per sync
#transfer logging = yes
log format = %t %a %m %f %b


[dui_resource]
path = /data/resources/dui_resource
list = yes
ignore errors
exclude = .svn/
EOF

/usr/bin/rsync --daemon --no-detach&
