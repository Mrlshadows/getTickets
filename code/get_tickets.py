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
from prettytable import PrettyTable
from colorama import init, Fore
from stations import stations

# 着色的初始化
init()

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

    # 获取持续时间，这个在哪里使用呢
    def _get_duration(self, raw_train):
        duration = raw_train.get('lishi').replace(':', '小时') + '分'
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    # 火车的数据
    @property
    def trains(self):
        for raw_train in self.available_trains:
            train_no = raw_train['station_train_code']
            initial = train_no[0].lower()
            if not self.options or initial in self.options:
                train = [
                    train_no,
                    '\n'.join([Fore.GREEN + raw_train['from_station_name' + Fore.RESET],
                               Fore.RED + raw_train['to_station_name'] + Fore.RESET]),
                    '\n'.join([Fore.GREEN + raw_train['start_time' + Fore.RESET],
                               Fore.RED + raw_train['arrive_time'] + Fore.RESET]),
                    self._get_duration(raw_train),
                    raw_train['zy_num'],
                    raw_train['ze_num'],
                    raw_train['rw_num'],
                    raw_train['yw_num'],
                    raw_train['yz_num'],
                    raw_train['wz_num'],
                ]
                yield train

    # 以表格形式打印数据
    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)



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

    # 可选项
    options = ''.join([
        key for key, value in arguments.items() if value is True
    ])

    # 访问获取result，并且格式化
    urllib3.disable_warnings()
    r = requests.get(url, verify=False)
    print(r.json())
    available_trains = r.json()['data']['result']
    TrainsPrase(available_trains, options).pretty_print()

# main 函数
if __name__ == '__main__':
    cli()