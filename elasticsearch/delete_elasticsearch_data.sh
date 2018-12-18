#!/bin/bash

timestamp=`date +%s`
es_addr='http://aispeech.elasticsearch.com:9200'

curl -XPUT -H "Content-Type: application/json" ${es_addr}/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'

indices_name=`curl ${es_addr}/_cat/indices?v|grep -E 'speechlog'|awk '{print $3}'`

for i in ${indices_name};
do
   indices_time=`echo $i|cut -d '-' -f 2|tr '.'  '-'`
   indices_timestamp=`date -d ${indices_time} +%s`
   time_diff=$[$timestamp - $indices_timestamp]
   if [[ ${time_diff} -gt 1296000 ]];then
       echo "delete indices" $i 
       curl -X DELETE ${es_addr}/${i}
   fi
done
