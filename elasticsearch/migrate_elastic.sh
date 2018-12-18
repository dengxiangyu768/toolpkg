#!/bin/bash
#author: dengxiangyu
#date: 2018-12-18


src_addr="http://src_elasticsearch.com:9200"
dst_addr="http://dst_elasticsearch.com:9200"

esindex=`curl --user ${user}:${password} ${src_addr}/_cat/indices?v|grep -v 'health'|grep -v kibana|awk '{print $3}'`

########## dump elastic ##########
#echo "---------------------"
for index in $esindex;
do
    /usr/bin/esm -s ${src_addr} -m ${user}:${password} -x $index -w=5 -b=10 -c 10000 --copy_settings --copy_mappings -o=/tmp/es/${index}.dump 
done

######### load elastic ##########

for index in $esindex;
do
   echo $index 
   /usr/bin/esm -d ${src_addr} -y $index -n ${user}:${password} -w=5 -b=10 -c 10000 --refresh -i=/tmp/es/${index}.dump
done

########## migrate elastic ##########
for index in $esindex;
do
    echo $index 
    /usr/bin/esm -s ${src_addr} -m ${user}:${password} -x $index  -d ${dst_addr} -n 'elastic':'AIspeech@)!^' -y $index -w=5 -b=10 -c 10000 --copy_settings --copy_mappings --force --refresh 
done
