#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   save_data_into_mysql.py
@Contact :   625711951@qq.com
@License :   (C)Copyright 2019-2020, Zyf-FT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/9/23 11:34   zyfei      1.0         None
'''

import pymysql
import time
from ../tools.mysql_connect import MysqlConnect
from queue import Queue

class SaveDataIntoMysql(object):
    ''''''
    def __init__(self):
        self.data_file = '../txt/position_df.csv'
        self.mysql_connect = MysqlConnect('lagou_data_shuju')
        self.base_sql = ''
        self.data_queue = Queue()

    def get_data_queue(self):
        with open(self.data_file, 'r', encoding='utf-8') as f:
            while True:
                position = f.readline()
                if not position:
                    break
                datas = position.split(';')
                self.data_queue.put(datas)

    def save_data_into_mysql(self):
        while True:
            if self.data_queue.empty():
                break
            datas = self.data_queue.get()
            insert_sql = 'insert into lagou_data_shuju_test(companyFullName, positionName, createTime, companyShortName, education, city, jobNature, industryField, financeStage, positionAdvantage, companySize, district, salary_min, salary_max) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
            self.mysql_connect.work_on_data(insert_sql, datas)
            self.data_queue.task_done()

    def run(self):
        self.get_data_queue()
        self.save_data_into_mysql()


if __name__ == '__main__':
    save_data_into_sql = SaveDataIntoMysql()
    save_data_into_sql.run()

