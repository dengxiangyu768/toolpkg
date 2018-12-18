#!/bin/bash
#date: 2017-11-23
cat<<\EOF >> /etc/rsyslog.conf 
$MaxMessageSize 256k
$ModLoad imudp.so
$UDPServerRun 514
local0.* /data/resources/log/mscp.log
local1.* /data/resources/log/nginx.log
local2.* /data/resources/log/scp.log
local3.* /data/resources/log/odcp-console.log
local4.* /data/resources/log/resserver.log
local5.* /data/resources/log/duiserver.log
local6.* /data/resources/log/access.log
local7.* /data/resources/log/audit.log
EOF


cat <<\EOF > /etc/logrotate.d/duilog
/data/log/*log
{
    daily
    rotate 14
    dateext
    create
    sharedscripts
    postrotate
        /bin/kill -HUP `cat /var/run/syslogd.pid 2> /dev/null` 2> /dev/null || true
    endscript
    compress
}
EOF
systemctl restart rsyslog

mkdir -p /opt/cron
cat <<\EOF > /opt/cron/logrotate.sh
#!/bin/sh
/usr/sbin/logrotate /etc/logrotate.conf >/dev/null 2>&1
EXITVALUE=$?
if [ $EXITVALUE != 0 ]; then
/usr/bin/logger -t logrotate "ALERT exited abnormally with [$EXITVALUE]"
fi
exit 0
EOF


echo "0 0 * * * /opt/cron/logrotate.sh" >> /var/spool/cron/root
