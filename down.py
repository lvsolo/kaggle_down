import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import pprint
import sys
import os
import json


print("python down.py search_tag store_path if_download")
ind = 1
search_tag = ''
store_path = ''
if_download = False
already_downloaded = 'downloaded_record'

if ind < len(sys.argv):
    search_tag=sys.argv[1]
    ind+= 1
if ind < len(sys.argv):
    store_path = sys.argv[2] + '/'
    ind += 1
if ind < len(sys.argv):
    if sys.arg[3] == "download":
        if_download = True
    ind += 1
api=KaggleApi()
api.authenticate()
store_path += '/'+search_tag + '/'

#api.competition_download_file('sentiment-analysis-on-movie-reviews','train.tsv.zip', path='./')
datasets = kaggle.api.datasets_list(search=search_tag)
for dt in datasets:
    print(dt['title'] +'||'+ dt['subtitleNullable'])


total_bytes = 0
for dt in datasets:
    total_bytes += dt['totalBytes']
print('total bytes:', total_bytes / 1024/1024, 'MB')
if if_download:
    with open('downloaded_record', 'a+') as f:
        lines = f.readlines()
        for dt in datasets:
            pprint.pprint(dt['ref'])
            if dt['ref'] in lines:
                continue
            else:
               f.write(dt['ref']+'\n')
            if not os.path.exists(store_path + dt['ref']):
                os.makedirs(store_path+dt['ref'])
            print('kaggle datasets download -d ' + dt['ref'] + ' -p ' + store_path + dt['ref'])
            os.system('kaggle datasets download -d ' + dt['ref'] + ' -p ' + store_path + dt['ref'])
            str_json = json.dumps(dt, indent=4)
            print(str_json, file=open(store_path + dt['ref'] + '/' + dt['ref'].split('/')[-1] + '.json', 'w'))
        f.close()
