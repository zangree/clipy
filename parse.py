#-*-coding:utf-8-*-
import re
from pprint import pprint
import requests

url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8955"

text = requests.get(url, verify=False)

stations = re.findall(r'([A-Z]+)\|([a-z]+)', text.text)

stations = dict(stations)
stations = dict(zip(stations.values(), stations.keys()))

# with open('statins.html', 'r', encoding='utf-8') as f:
#     text = f.read()
# stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', text)

pprint(dict(stations), indent=4)
