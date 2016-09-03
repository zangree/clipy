#-*-coding:utf-8-*-
"""
Train tickets query via command-line.

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h, --help  显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 南京 北京 2016-07-01
"""
from docopt import docopt
import requests
from prettytable import PrettyTable
from stations import stations
import re


def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    # 构建URL
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(
        date, from_staion, to_station
    )

    # 添加verify=False参数不验证证书
    r = requests.get(url, verify=False)
    rows = r.json()['data']['datas']
    trains = TrainCollection(rows)
    trains.pretty_print()


class TrainCollection(object):
    headers = '车次 车站 时间 历时 商务 一等 二等 软卧 硬卧 软座 硬座 无座'.split()

    def __init__(self, rows):
        self.rows = rows

    def _get_duration(self, row):
        """
        获取车次运行时间
        """
        duration = row.get('历时').replace(':', 'h') + 'm'
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    @property
    def trains(self):
        for row in self.rows:
            train = [
                #车次
                row['station_train_code'],
                #出发、到达站
                # '\n'.join(['from_station_name'], row['to_station_name']),
                '\n'.join([colored('green', row['from_station_name']),
                           colored('red', row['to_station_name'])]),
                #出发、到达时间
                # '\n'.join(['start_time'], row['arrive']),
                '\n'.join([colored('green', row['start_time']),
                           colored('red', row['arrive_time'])]),
                #历时
                self._get_duration(row),
                #一等座
                row['zy_num'],
                #二等座
                row['ze_num'],
                #软卧
                row['rw_num'],
                #软座
                row['yw_num'],
                #硬座
                row['yz_num']
            ]
            yield train

    def pretty_print(self):
        """

        """
        pt = PrettyTable()
        #设置每一列的标题
        pt._set_field_names(self.headers)
        for train in self.trains:
            pt.add_row(train)
        print(pt)


def colored(color, text):
    talbe = {
        'red': '\033[91m',
        'green': '\033[92m',
        # no color
        'nc': '\033[0'
    }
    cv = table.get(color)
    nc = table.get('nc')
    return ''.join([cv, text, nc])

if __name__ == '__main__':
    cli()
