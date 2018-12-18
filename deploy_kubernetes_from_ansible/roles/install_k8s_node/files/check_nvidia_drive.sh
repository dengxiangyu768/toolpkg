#!/bin/bash



function is_error(){
  result=$1
  message=$2
  if [[ $result -ne 0 ]]
    echo $2 > pre_install_nvidia.log 
    exit 1
  fi
}

rmmod nouveau
is_error $? "rmmod nouveau error"

echo "blacklist nouveau" >> /etc/modprobe.d/blacklist.conf
is_error $? "blacklist nouveau error"

mv /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r).img.bak
is_error $? "mv img error"

dracut -v /boot/initramfs-$(uname -r).img $(uname -r)
is_error $? "mv img error"
