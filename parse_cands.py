import argparse
import pickle
import json
import requests
from datetime import datetime, timedelta

parser = argparse.ArgumentParser(description='Extract, transform and load veryfast candidate data.')
parser.add_argument('-f', '--filename', type=str, dest='filename', required=True, help='candidate filename in pickle format')

# Set arguments to appropriate variable
args = parser.parse_args()
file = args.filename
alldata = []

with open(file) as pkl:
  state = pickle.load(pkl)
  cands = pickle.load(pkl)

# Generate dumy dates
alldata = []
time = datetime.now()
date = time;
for key in cands:
  data = {}
  date = date + timedelta(hours=1)
  data['obs'] = '14A-425'
  data['@timestamp'] = date.isoformat()+'Z'
  data['scan'] = key[0]
  data['segment'] = key[1]
  data['integration'] = key[2]
  data['dm'] = key[3]
  data['dt'] = key[4]
  value = cands[key]
  data['snr'] = value[0]
  idobj = {}
  idobj['_id'] = data['obs'] + '_' + str(data['scan']) + '_' + str(data['segment'])+ '_' + str(data['integration'])
  # print data

  alldata.append({"index":idobj})
  alldata.append(data)

jsonStr = json.dumps(alldata,separators=(',', ':'))
cleanjson = jsonStr.replace('}},','}}\n').replace('},','}\n').replace(']','').replace('[','')
print cleanjson
url = 'http://localhost:9200/veryfast/cands/_bulk?'
r = requests.post(url, data=cleanjson)
print r
