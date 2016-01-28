import argparse
import json
import requests
from datetime import datetime

parser = argparse.ArgumentParser(description='Extract, transform and load veryfast log data.')
parser.add_argument('--log', type=str, dest='log', required=True, help='log filename')
# Set arguments to appropriate variable
args = parser.parse_args()
log_file = args.log
alldata = []

with open(log_file) as file:
  f = file.readlines()
  for line in f:
    # Create object to push as json source 
    segment = line.split(' - ')
    if len(segment) == 4 :
      if datetime.strptime(segment[0], '%Y-%m-%d %H:%M:%S,%f') :
        data = {}
        date = datetime.strptime(segment[0], '%Y-%m-%d %H:%M:%S,%f')

        # Create id object (required for elastic bulk push)
        idobj = {}
        idobj['_id'] = date.isoformat() +'Z'
        data['@timestamp'] = date.isoformat() +'Z'
        data['system'] = segment[1]
        data['level'] = segment[2]
        data['message'] = segment[3]

        # Push object with unique '_id' into main object
        alldata.append({"index":idobj})
        alldata.append(data)

    
jsonStr = json.dumps(alldata,separators=(',', ':'))
cleanjson = jsonStr.replace('},','}\n').replace(']','').replace('[','')
print cleanjson

url = 'http://localhost:9200/vflogs/_bulk?'
r = requests.post(url, data=cleanjson)
print r
