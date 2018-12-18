#!/usr/bin/env python 
#up
#uptime
#health 
#memusage

# status: 0 is normal, !0 is abnormal
import httplib
import urllib
import urllib2
import os
import json
import base64
import sys 
import shutil

Debug = False

es_addr_list = [ 
           ('dui-log-elasticsearch','http://10.12.183.90:9200'),\
           ('dui-prod-elasticsearch','http://elasticsearch.com:9200','username','password')
          ]   

class ElasticSearchHealth(object):
  def __init__(self,addr):
    self.addr = addr
    self.metric_name = 'duimonitor_elasticsearch'
    self.headers = {"Content-Type":"application/json"}
    self.cluster_health = None
    self.cluster_nodes = None
    self.nodes_nodes = None
    self.es_addr = self.addr[1]
    self.es_name = self.addr[0]
    if len(addr) == 4:
      self.key =  self.addr[2]
      self.secret = self.addr[3]
    else:
      self.key = None
      self.secret = None

  def output_metric(self,model,value):
    print ("%s{es_name=\"%s\",mode=\"%s\"} %s" \
    %(self.metric_name,self.es_name,model,value)).strip()

  def output_jvm_metric(self,node,model,value):
      print ("%s{es_name=\"%s\",node=\"%s\",mode=\"%s\"} %s" \
      %(self.metric_name,self.es_name,node,model,value)).strip()

  def query(self,api):
    url = self.es_addr + api
    try:
      request = urllib2.Request(url)
      request.add_header("Content-Type","application/json")
      if self.key  and self.secret:
        base64string = base64.b64encode('%s:%s' % (self.key, self.secret))
        request.add_header("Authorization", "Basic %s" % base64string)
      response = urllib2.urlopen(request)
      result = json.loads(response.read())
      return result
    except:
      return False 

  def available(self):
    self.cluster_health = self.query("/_cluster/health")
    self.cluster_stats = self.query("/_cluster/stats")
    self.nodes_stats = self.query("/_nodes/stats")
   
    if self.cluster_health and self.cluster_stats and self.nodes_stats:
      self.output_metric("available",0)
      return True
    else:
      self.output_metric("available",1)
      return False

  def get_cluster_health(self):
    if self.cluster_health['status'] == 'green':
      self.output_metric("health",0)
    elif self.cluster_health['status'] == 'yellow':
      self.output_metric("health",1)
    else:
      self.output_metric("health",2)

      self.output_metric('initializing_shards',-1)



  def get_nodes_indices(self):
    try:
      if self.nodes_stats.has_key('nodes'):
        for key,value in self.nodes_stats['nodes'].items():
          nodename = value['name']
          docs = value['indices']['docs']['count']
          store = value['indices']['store']['size_in_bytes']
          query_total = value['indices']['search']['query_total']
          query_time_in_millis = value['indices']['search']['query_time_in_millis']
          query_current = value['indices']['search']['query_current']
          fetch_total = value['indices']['search']['fetch_total']
          fetch_time_in_millis = value['indices']['search']['fetch_time_in_millis']
          fetch_current = value['indices']['search']['fetch_current']
          index_total = value['indices']['indexing']['index_total']
          index_time_in_millis = value['indices']['indexing']['index_time_in_millis']
          index_current = value['indices']['indexing']['index_current']
          refresh_total = value['indices']['refresh']['total']
          refresh_total_time = value['indices']['refresh']['total_time_in_millis']
          flush_total = value['indices']['flush']['total']
          flush_total_time = value['indices']['flush']['total_time_in_millis']
          http_current_open = value['http']['current_open']
          http_total_open = value['http']['total_opened']
          self.output_jvm_metric(nodename,"docs",docs)
          self.output_jvm_metric(nodename,"store",store)
          self.output_jvm_metric(nodename,"query_total",query_total)
          self.output_jvm_metric(nodename,"query_time_in_millis",query_time_in_millis)
          self.output_jvm_metric(nodename,"query_current",query_current)
          self.output_jvm_metric(nodename,"fetch_total",fetch_total)
          self.output_jvm_metric(nodename,"fetch_time_in_millis",fetch_time_in_millis)
          self.output_jvm_metric(nodename,"fetch_time_current",fetch_current)
          self.output_jvm_metric(nodename,"index_total",index_total)
          self.output_jvm_metric(nodename,"index_time_in_millis",index_time_in_millis)
          self.output_jvm_metric(nodename,"index_current",index_current)
          self.output_jvm_metric(nodename,"refresh_total",refresh_total)
          self.output_jvm_metric(nodename,"refresh_total_time",refresh_total_time)
          self.output_jvm_metric(nodename,"flush_total",flush_total)
          self.output_jvm_metric(nodename,"flush_total_time",flush_total_time)
          self.output_jvm_metric(nodename,"http_current_open",http_current_open)
          self.output_jvm_metric(nodename,"http_total_open",http_total_open)
          heap_used_percent = value['jvm']['mem']['heap_used_percent']
          heap_used_in_bytes = value['jvm']['mem']['heap_used_in_bytes']
          heap_max_in_bytes = value['jvm']['mem']['heap_max_in_bytes']
          young_used_in_bytes = value['jvm']['mem']['pools']['young']['used_in_bytes']
          young_max_in_bytes = value['jvm']['mem']['pools']['young']['max_in_bytes']
          survivor_used_in_bytes = value['jvm']['mem']['pools']['survivor']['used_in_bytes']
          survivor_max_in_bytes = value['jvm']['mem']['pools']['survivor']['max_in_bytes']
          old_used_in_bytes = value['jvm']['mem']['pools']['old']['used_in_bytes']
          old_max_in_bytes = value['jvm']['mem']['pools']['old']['max_in_bytes']
          gc_young_collection = value['jvm']['gc']['collectors']['young']['collection_count']
          gc_old_collection = value['jvm']['gc']['collectors']['old']['collection_count']
          self.output_jvm_metric(nodename,"heap_used_percent",heap_used_percent)
          self.output_jvm_metric(nodename,"heap_used_in_bytes",heap_used_in_bytes)
          self.output_jvm_metric(nodename,"heap_max_in_byte",heap_used_in_bytes)
          self.output_jvm_metric(nodename,"young_used_in_bytes",young_used_in_bytes)
          self.output_jvm_metric(nodename,"young_max_in_bytes",young_max_in_bytes)
          self.output_jvm_metric(nodename,"survivor_used_in_bytes",survivor_used_in_bytes)
          self.output_jvm_metric(nodename,"survivor_max_in_bytes",survivor_max_in_bytes)
          self.output_jvm_metric(nodename,"old_used_in_bytes",old_used_in_bytes)
          self.output_jvm_metric(nodename,"old_max_in_bytes",old_max_in_bytes)
          self.output_jvm_metric(nodename,"gc_young_collection",gc_young_collection)
          self.output_jvm_metric(nodename,"gc_old_collection",gc_old_collection)
          thread_pool_bulk_queue = value['thread_pool']['bulk']['queue']
          thread_pool_index_queue = value['thread_pool']['index']['queue']
          thread_pool_search_queue = value['thread_pool']['search']['queue']
          thread_pool_merge_queue = value['thread_pool']['force_merge']['queue']
          thread_pool_bulk_rejected = value['thread_pool']['bulk']['rejected']
          thread_pool_index_rejected = value['thread_pool']['index']['rejected']
          thread_pool_search_rejected = value['thread_pool']['search']['rejected']
          thread_pool_merge_rejected = value['thread_pool']['force_merge']['rejected']
          self.output_jvm_metric(nodename,"thread_pool_bulk_queue",thread_pool_bulk_queue)
          self.output_jvm_metric(nodename,"thread_pool_index_queue",thread_pool_index_queue)
          self.output_jvm_metric(nodename,"thread_pool_search_queue",thread_pool_search_queue)
          self.output_jvm_metric(nodename,"thread_pool_merge_queue",thread_pool_merge_queue)
          self.output_jvm_metric(nodename,"thread_pool_bulk_rejected",thread_pool_bulk_rejected)
          self.output_jvm_metric(nodename,"thread_pool_index_rejected",thread_pool_index_rejected)
          self.output_jvm_metric(nodename,"thread_pool_search_rejected",thread_pool_search_rejected)
          self.output_jvm_metric(nodename,"thread_pool_merge_rejected",thread_pool_merge_rejected)
          total_in_bytes = value['fs']['total']['total_in_bytes']
          free_in_bytes = value['fs']['total']['free_in_bytes']
          available_in_bytes = value['fs']['total']['available_in_bytes']
          read_operations = value['fs']['io_stats']['total']['read_operations']
          write_operations = value['fs']['io_stats']['total']['write_operations']
          read_kilobytes = value['fs']['io_stats']['total']['read_kilobytes']
          write_kilobytes = value['fs']['io_stats']['total']['write_kilobytes']
          self.output_jvm_metric(nodename,"total_in_bytes",total_in_bytes)
          self.output_jvm_metric(nodename,"free_in_bytes",free_in_bytes)
          self.output_jvm_metric(nodename,"available_in_bytes",available_in_bytes)
          self.output_jvm_metric(nodename,"read_operations",read_operations)
          self.output_jvm_metric(nodename,"write_operations",write_operations)
          self.output_jvm_metric(nodename,"read_kilobytes",read_kilobytes)
          self.output_jvm_metric(nodename,"write_kilobytes",write_kilobytes)
    except:
      self.output_jvm_metric(nodename,-1)


  def get_cluster_nodes(self):
    if self.cluster_stats.has_key('_nodes'):
      total_nodes = self.cluster_stats['_nodes']['total']
      successful_nodes = self.cluster_stats['_nodes']['successful']
      self.output_metric("total_nodes",total_nodes)
      self.output_metric("successful_nodes",successful_nodes)
      unassigned_shards = self.cluster_health['unassigned_shards']
      active_shards_percent_as_number = self.cluster_health['active_shards_percent_as_number']
      relocating_shards = self.cluster_health['relocating_shards']
      active_primary_shards = self.cluster_health['active_primary_shards']
      active_shards = self.cluster_health['active_shards']
      initializing_shards = self.cluster_health['initializing_shards']
      self.output_metric('unassigned_shards',unassigned_shards)
      self.output_metric('active_shards_percent_as_number',active_shards_percent_as_number)
      self.output_metric('relocating_shards',relocating_shards)
      self.output_metric('active_primary_shards',active_primary_shards)
      self.output_metric('active_shards',active_shards)
      self.output_metric('initializing_shards',initializing_shards)
    else:
      self.output_metric("total_nodes",-1)
      self.output_metric("successful_nodes",-1)



  def get_query_hit_precent(self):
    if self.cluster_stats['nodes']['jvm']['max_uptime_in_millis']:
      total_count = float(self.cluster_stats['indices']['query_cache']['total_count'])
      hit_count = self.cluster_stats['indices']['query_cache']['hit_count']
      query_cache_hit_precent = hit_count / total_count
      self.output_metric("query_hit_precent",query_cache_hit_precent)
    else:
      self.output_metric("query_hit_precent",-1)


  def get_cluster_mem_usage(self):
    if self.cluster_stats['nodes']['os']['mem']['used_percent']:
      cluster_mem_usage = self.cluster_stats['nodes']['os']['mem']['used_percent']
    else:
      cluster_mem_usage = -1
    self.output_metric("cluster_mem_usage",cluster_mem_usage)



def main():
  sys.stdout = open("/tmp/monitor_elasticsearch.log","w")
  for es_addr in es_addr_list:
    clusterhealth = ElasticSearchHealth(es_addr)
    if clusterhealth.available():
      clusterhealth.get_cluster_health()
      clusterhealth.get_cluster_nodes()
      clusterhealth.get_nodes_indices()
  sys.stdout.flush()
  shutil.move("/tmp/monitor_elasticsearch.log","/tmp/latest_elasticsearch.log")   
if __name__ == '__main__':
  main()
