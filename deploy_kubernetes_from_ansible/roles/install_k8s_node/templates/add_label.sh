#!/bin/bash
label_name={{ service }}
apiserver={{ apiserver_load_balance_ip }}
curl -k -H "Accept: application/json" -XPATCH -d '{"metadata":{"labels":{"${label_name}":"1"}}}' -H "Content-Type: application/merge-patch+json" 'http://${apiserver}:6443/api/v1/nodes/'$host

