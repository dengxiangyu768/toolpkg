#!/usr/bin/python
#author:dengxiangyu
#date: 2018-07-10
#coding:utf-8

import httplib
import os
import json
import time
import shutil
import sys



def request(timestamp,body,api):
  result = None
  try:
    conn = httplib.HTTPConnection("10.15.12.95",9200,False)
    conn.request('get',api,body,{"Content-Type":"application/json"})
    response =  conn.getresponse().read()
    result = json.loads(response)
  except Exception as e:
    print e
  return result

def cal_ddsserver():
  result = None
  timestamp = int(time.time())
  index_time = time.strftime("%Y.%m.%d",time.localtime(timestamp))
  api = "/cleanning-log-dui-rsyslog-audit-%s/_search" %(index_time)
  body = '{ "size":0, "query":{ "range":{ "@timestamp":{ "gte":"now-5m" } } }, "aggs":{ "dm_latency_percentiles":{ "percentiles":{ "field":"dm_duration", "percents":[50,90,95] } }, "ssm_latency_percentiles":{ "percentiles":{ "field":"ssmserver", "percents":[50,90,95] } }, "asr_latency_percentiles":{ "percentiles":{ "field":"asr_duration", "percents":[50,90,95] } }, "skillDispatch_latency_percentiles":{ "percentiles":{ "field":"skillDispatch", "percents":[50,90,95] } }, "total_latency_percentiles":{ "percentiles":{ "field":"total_duration", "percents":[50,90,95] }}, "webhook_latency_percentiles":{ "percentiles":{ "field":"webhook","percents":[50,90,95]}}, "total_durationd_avg":{ "avg":{ "field":"total_duration"}}, "dm_durationd_avg":{ "avg":{ "field":"dm_duration"}}, "ssm_durationd_avg":{ "avg":{ "field":"ssmserver"}}, "asr_durationd_avg":{ "avg":{ "field":"asr_duration"}}, "skillDispatch_durationd_avg":{ "avg":{ "field":"skillDispatch" } },"tts_duration_avg":{"avg":{"field":"tts_duration"}},"tts_duration_percentiles":{"percentiles":{"field":"tts_duration","percents":[50,90,95]}},"aios_duration_percentiles":{"percentiles":{"field":"aios_duration","percents":[50,90,95]}},"nlu_duration_percentiles":{"percentiles":{"field":"nlu_duration","percents":[50,90,95]}} } }' 
  result = request(timestamp,body,api)
  if result:
    for key,value in result['aggregations'].items():
      if value.has_key('values'):
        print ("service_duration{latency=\"%s\",mode=\"pt50\"} %s" %(key.split('_')[0],value["values"]["50.0"])).strip()
        print ("service_duration{latency=\"%s\",mode=\"pt90\"} %s" %(key.split('_')[0],value["values"]["90.0"])).strip()
        print ("service_duration{latency=\"%s\",mode=\"pt95\"} %s" %(key.split('_')[0],value["values"]["95.0"])).strip()
 
def cal_sub_service():
  result = None
  timestamp = int(time.time())
  index_time = time.strftime("%Y.%m.%d",time.localtime(timestamp))
  api = "/cleanning-log-dui-rsyslog-duiserver-%s/_search" %(index_time)
  body =  '{ "size":0, "query":{ "bool": { "filter": { "range": { "@timestamp": { "gte": "now-5m" } } }, "must_not": [ {"term": { "module.keyword": "qps" }}, {"term": { "module.keyword": "hotword" }} ] } }, "aggs":{ "service_name":{ "terms":{ "field":"service.keyword" }, "aggs":{ "service_duration":{ "percentiles":{ "field":"request_time","percents": [50,90,95] } } } } } }' 
  result = request(timestamp,body,api)
  if result:
    result = result['aggregations']['service_name']['buckets']
    for i in result: 
      service = i['key']
      if service == 'cnlu':
        service = 'cnlusvr'
      print ("service_duration{latency=\"%s\",mode=\"pt50\"} %s" %(service,i['service_duration']['values']['50.0'])).strip()
      print ("service_duration{latency=\"%s\",mode=\"pt90\"} %s" %(service,i['service_duration']['values']['90.0'])).strip()
      print ("service_duration{latency=\"%s\",mode=\"pt95\"} %s" %(service,i['service_duration']['values']['95.0'])).strip()

def cal_cdmserver_service():
  pt50 = 0
  pt90 = 0 
  pt95 = 0
  result = None
  timestamp = int(time.time())
  index_time = time.strftime("%Y.%m.%d",time.localtime(timestamp))
  api = "/cleanning-log-dui-rsyslog-cdmserver-%s/_search" %(index_time)
  body = '{ "size":0, "query":{ "range":{ "@timestamp":{ "gte":"now-5m" } } }, "aggs":{ "cdm_latency_percentiles":{ "percentiles":{ "field":"cdm_duration", "percents":[50,90,95] } }}}'
  result = request(timestamp,body,api)
  if result:
    for key,value in result['aggregations'].items():
      if value.has_key('values'):
        if value["values"]["50.0"] != 'NaN':
          pt50 = value["values"]["50.0"] 
        if value["values"]["90.0"] != 'NaN':
          pt90 = value["values"]["90.0"] 
        if value["values"]["95.0"] != 'NaN':
          pt95 = value["values"]["95.0"] 
        print ("service_duration{latency=\"%s\",mode=\"pt50\"} %s" %(key.split('_')[0],pt50)).strip()
        print ("service_duration{latency=\"%s\",mode=\"pt90\"} %s" %(key.split('_')[0],pt90)).strip()
        print ("service_duration{latency=\"%s\",mode=\"pt95\"} %s" %(key.split('_')[0],pt95)).strip()
 

def cal_dm_dispatch_service():
  pt50 = 0
  pt90 = 0 
  pt95 = 0
  result = None
  timestamp = int(time.time())
  index_time = time.strftime("%Y.%m.%d",time.localtime(timestamp))
  api = "/cleanning-log-dui-rsyslog-dm-dispatch-%s/_search" %(index_time)
  body = ' { "size":0, "query":{ "range":{ "@timestamp":{ "gte":"now-5m" } } }, "aggs":{ "ba_latency_percentiles":{ "percentiles":{ "field":"ba_duration", "percents":[50,90,95] }}, "dmdispatch_latency_percentiles":{ "percentiles":{ "field":"dmdispatch_duration", "percents":[50,90,95] } } } }'
  result = request(timestamp,body,api)
  if result:
    for key,value in result['aggregations'].items():
      if value.has_key('values'):
        if value["values"]["50.0"] != 'NaN':
          pt50 = value["values"]["50.0"] 
        if value["values"]["90.0"] != 'NaN':
          pt90 = value["values"]["90.0"] 
        if value["values"]["95.0"] != 'NaN':
          pt95 = value["values"]["95.0"] 
        print ("service_duration{latency=\"%s\",mode=\"pt50\"} %s" %(key.split('_')[0],pt50)).strip()
        print ("service_duration{latency=\"%s\",mode=\"pt90\"} %s" %(key.split('_')[0],pt90)).strip()
        print ("service_duration{latency=\"%s\",mode=\"pt95\"} %s" %(key.split('_')[0],pt95)).strip()


def main(): 
  cal_ddsserver()
  cal_sub_service()
  cal_dm_dispatch_service()
  cal_cdmserver_service()
      

if __name__ == '__main__':
  main()
