# -*- coding: utf-8 -*-
# __Author__: Mr.shadow

import re
import requests
from pprint import pprint

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971'

# 获取返回数据
response = requests.get(url, verify=False)
# 正则表达式提取中文字母和代号
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)

# 格式化输出数据
pprint(dict(stations), indent=4)