#!/usr/bin/python
#!coding:utf-8
#author: dengxiangyu

######
# 1. consumer data
# 2. cleaning data
# 3. push data
#####

import json
import os
import sys
from kafka import KafkaConsumer
import time
import httplib
import uuid

Debug = True 

class Consumer(object):
  def __init__(self,group,topic):
    self.group = group
    self.topic = topic
    self.kafka_addr = "10.12.183.187:9092,10.12.183.189:9092,10.12.183.188:9092" 
    self.elastic_addr = "10.15.12.95:9200" 
    self.data = '' 
 
  def start(self):
    if Debug:
      print "start consumer..."
    consumer = KafkaConsumer(self.topic,group_id=self.group,bootstrap_servers = self.kafka_addr)
    for message in consumer:
      value =  message.value
      value_str = json.loads(value)['message']
      self.data_cleaning(value_str)
      #print value_str


  def data_cleaning(self,message):
    try:
      if ("AnalysisLog" in message) and ("request_time" in message) and \
         ("wavetime" in message) and ("asctime" in message) and ("aiwechat" in message):
        left = message.find("|")
        right = message.rfind("}")
        result = {}
        if (left > 0) and (right > 0):
          body = message[left+1:right+1].split('|')
          jsons = json.loads(body[-1])
          result['host'] = body[0]           
          result['server'] = "aiwechat" 
          result['status'] = jsons['status']
          result['request_time'] = jsons['request_time']
          result['wavetime'] = jsons['response']['wavetime']
          timestamp =  int(float(jsons['asctime'].encode('utf-8'))) - 28800
          result['@timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%SZ',time.localtime(timestamp))
          localtime = time.strftime("%Y.%m.%d",time.localtime())
          es_name =  self.group + '-' + localtime
          es_meta = { "create" : { "_index" : es_name, "_type" : "doc" , "_id": uuid.uuid1().int} }
          result = json.dumps(es_meta) + '\n' + json.dumps(result)
          self.upload(result)     
    except Exception as e:
      print e 


    
  def upload(self,result):
    self.data = self.data + '\n' + result
    if len(self.data) > 5000:
      self.data = self.data + "\n"
      response_code = self.request() 
      print time.asctime(),response_code
      if response_code == 200:
         self.data = '' 
           
  def request(self): 
    try:
      es_api = "/_bulk"
      url = self.elastic_addr 
      headers = {"Content-Type":"application/json"}
      params = self.data 
      conn = httplib.HTTPConnection(url)
      conn.request("POST", es_api, params, headers)
      response = conn.getresponse()
      return response.status
    except Exception as e:
      print "exception error"
      print e 
   
def main():
  consumer = Consumer('log-dui-rsyslog-nginx-aiwechat-cleaning','log-dui-rsyslog-nginx')
  consumer.start() 

if __name__ == '__main__': 
  main()
