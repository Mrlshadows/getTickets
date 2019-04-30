# -*- coding: utf-8 -*-
# __Author__: Mr.shadow

"""火车票查询工具

Usage:
    tickets [-gdtkz] <from> <to> <date>

注意：Usage为固定词汇，其他报错。

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 大同 2016-08-28
    tickets -t 北京 大同 2016-08-28
"""
from docopt import docopt
import requests
import urllib3
import prettytable
import colorama
from stations import stations

# 解析数据类
class TrainsPrase:
    # 解析数据的标题
    header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()

    # 构造函数
    def __init__(self, available_trains, options):
        # available_trains 存储火车班次列表
        self.available_trains = available_trains
        # options 存储查询的选项，高铁，动车等
        self.options = options

    # 获取持续时间
    def _get_duration(self, raw_train):
        duration = raw_train.get('lishi').replace(':', '小时') + '分'
        if duration.startswith('00')

# 命令行接口
def cli():

    # 获取参数
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']

    # 构建URL
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_station, to_station
    )

    # 访问获取result
    urllib3.disable_warnings()
    r = requests.get(url, verify=False)
    print(r.json()['data']['result'])

# main 函数
if __name__ == '__main__':
    cli()