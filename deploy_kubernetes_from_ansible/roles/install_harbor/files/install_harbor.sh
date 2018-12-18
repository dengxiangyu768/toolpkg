#!/bin/sh
#date: 2017-11-07


function install_docker()
{
    cd /tmp 
    wget http://aliacs-k8s.oss-cn-hangzhou.aliyuncs.com/rpm/docker-1.12.6/docker-engine-selinux-1.12.6-1.el7.centos.noarch.rpm
    wget http://aliacs-k8s.oss-cn-hangzhou.aliyuncs.com/rpm/docker-1.12.6/docker-engine-1.12.6-1.el7.centos.x86_64.rpm
    yum localinstall  -y docker-engine-selinux-1.12.6-1.el7.centos.noarch.rpm docker-engine-1.12.6-1.el7.centos.x86_64.rpm

    sed -i "s#ExecStart=/usr/bin/dockerd#ExecStart=/usr/bin/dockerd -D -H tcp://0.0.0.0:27000 -H unix:///var/run/docker.sock -g /data/docker -D --insecure-registry dui.lenovo.com.cn  --registry-mirror=https://pqbap4ya.mirror.aliyuncs.com#g" /lib/systemd/system/docker.service
    systemctl enable docker.service
    systemctl restart docker.service
    
}

function install_docker-compose()
{
    cd /tmp
    wget http://7xp70x.com1.z0.glb.clouddn.com/docker-compose
    cp docker-compose /usr/local/bin/
    chmod +x /usr/local/bin/docker-compose
}

function install_harbor()
{
    cd /tmp 
    mkdir -p /data/resources
    wget http://7xp70x.com1.z0.glb.clouddn.com/harbor_0.5.0.tar.gz 
    tar -zxvf harbor_0.5.0.tar.gz -C /data/resources/
    cd /data/resources/harbor/make/
    bash install.sh
}


main()
{
    install_docker-compose
    install_harbor
}

main
