# VLA Project - Extract, transform, and load (ETL)

This documentaion describes how to Extract, transform, and load candidate files for VLA.

Here we are assuming that the backend is using Elasticsearch.
After following the instruction found on ES site, continue with the following setup guide:
https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html

#### Custom setup for RF ElasticSearch
###### Add the following lines to elasticsearch.yml found in the config directory:
```
http.cors.enabled:true
http.cors.allow-origin : “*” // *IMPORTANT* change this when in operations
http.cors.allow-methods : OPTIONS, HEAD, GET, POST, PUT, DELETE
http.cors.allow-headers : X-Requested-With,X-Auth-Token,Content-Type, Content-Length
```

###### Start ES from bin directory (using version 2.1.1)
```
./elasticsearch --cluster.name my_cluster_name --node.name my_node_name
```

#### Custom setup for RF ElasticSearch

###### Start ES in bin directory
```
./elasticsearch --cluster.name realfast --node.name candidate_data
```

###### Create ES ‘cand’ index and push that from cands file:
```
curl -XPUT 'localhost:9200/cand?pretty'
python parse_cands.py  -f cands_14A-425_14sep03_stats_merge.pkl
```

###### Can view ES index by going to the following URL:
```
http://localhost:9200/cand/_search?q=*&pretty - display everything in index
```

##### General Info

###### Command
```
curl -X<REST Verb> <Node>:<Port>/<Index>/<Type>/<ID>
```

###### List of nodes in cluster
```
curl 'localhost:9200/_cat/nodes?v'
```

###### Check health
```
curl 'localhost:9200/_cat/health?v'
```

##### Examples
```
curl -XPUT 'localhost:9200/customer'
curl -XPUT 'localhost:9200/customer/external/1' -d '
{
  "name": "John Doe"
}'
curl 'localhost:9200/customer/external/1'
curl -XDELETE 'localhost:9200/customer'
```
