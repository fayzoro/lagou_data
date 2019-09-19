#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   save_position_to_txt.py    
@Contact :   zyf.912@163.com
@License :   (C)Copyright 2019-2020, ZYF-FT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/9/17 21:13   zyfei      1.0         None
'''

import os
import json
from queue import Queue
from threading import Thread


class JsonToTxt(object):
    ''''''
    def __init__(self):
        ''''''
        self.html_source_dir = '../html/'
        self.save_txt_dir = '../txt/'
        self.file_queue = Queue()
        self.html_queue = Queue()
        self.position_queue = Queue()
        self.threadings = []

    def get_file_queue(self):
        '''
        从源目录中找出指定文件，放入队列之中
        无参数
        :return: None
        '''
        file_list = os.listdir(self.html_source_dir)
        for file_name in file_list:
            if file_name.endswith('.html'):
                # 设置网页的相对路径
                file_path = self.html_source_dir + file_name
                self.file_queue.put(file_path)

    def get_html_queue(self):
        '''
        获取每一张网页的内容，放入队列之中
        无参数
        :return: None
        '''
        while True:
            if self.file_queue.empty():
                break
            file_path = self.file_queue.get()
            with open(file_path, 'r', encoding='utf-8') as f:
                html = f.read()
                print(file_path, '文件内容获取成功')
                self.html_queue.put(html)
            self.file_queue.task_done()

    def get_positions_queue_from_html(self):
        '''
        分析网页获取职位信息， 放入职位队列
        无参数
        :return: None
        '''
        while True:
            if self.html_queue.empty() and self.file_queue.empty():
                break
            html = self.html_queue.get()
            # 将字符串对象转换成json字典
            html_dict = json.loads(html)
            # 解析职位信息，放入列表
            positions = []
            # pageNo = html_dict["content"]['pageNo']
            # 解析职位信息
            positionResult = html_dict["content"]['positionResult']
            position_list = positionResult['result']
            for pos in position_list:
                # 职位， 地点， 年薪， 经验，发布时间，学历，公司名字，类型，等级，人数，评论
                position = {}
                # 公司全名
                position['companyFullName'] = pos['companyFullName']
                # 职位名称
                position['positionName'] = pos['positionName']
                # 发布时间
                position['createTime'] = pos['createTime']
                # 公司简称
                position['companyShortName'] = pos['companyShortName']
                # 公司地点
                position['city'] = pos['city']
                # 教育程度
                position['education'] = pos['education']
                # 是否全职
                position['jobNature'] = pos['jobNature']
                # 年薪
                position['salary'] = pos['salary']
                # 类型
                position['industryField'] = pos['industryField']
                # 融资阶段
                position['financeStage'] = pos['financeStage']
                # 职位优势
                position['positionAdvantage'] = pos['positionAdvantage']
                # 公司人数规模
                position['companySize'] = pos['companySize']
                # 公司福利待遇
                position['companyLabelList'] = pos['companyLabelList']
                # 公司办公地区
                position['district'] = pos['district']
                # 职位标签
                position['positionLables'] = pos['positionLables']
                positions.append(position)
            self.position_queue.put(positions)
            self.html_queue.task_done()

    def save_positions_into_txt(self):
        '''
        将职位信息存入txt文件
        无参数
        :return: None
        '''
        while True:
            if self.position_queue.empty() and self.html_queue.empty() and self.file_queue.empty():
                break
            # 设置文本保存路径
            save_position_file_name = self.save_txt_dir + 'positions_test.txt'
            positions = self.position_queue.get()
            for position in positions:
                msg = str(position['companyFullName']) + ';'
                msg += str(position['positionName']) + ';'
                msg += str(position['createTime']) + ';'
                msg += str(position['companyShortName']) + ';'
                msg += str(position['city']) + ';'
                msg += str(position['education']) + ';'
                msg += str(position['jobNature']) + ';'
                msg += str(position['salary']) + ';'
                msg += str(position['industryField']) + ';'
                msg += str(position['financeStage']) + ';'
                msg += str(position['positionAdvantage']) + ';'
                msg += str(position['companySize']) + ';'
                msg += str(position['companyLabelList']) + ';'
                msg += str(position['district']) + ';'
                msg += str(position['positionLables']) + '\n'
                with open(save_position_file_name, 'a', encoding='utf-8') as f:
                    f.write(msg)
            self.position_queue.task_done()

    def make_threadings(self):
        '''
        创建多个线程同时运行，提高io时间效率
        无参数
        :return: None
        '''
        for _i in range(4):
            t1 = Thread(target=self.get_html_queue)
            self.threadings.append(t1)
        for _j in range(4):
            t2 = Thread(target=self.get_positions_queue_from_html)
            self.threadings.append(t2)
        for _k in range(4):
            t3 = Thread(target=self.save_positions_into_txt)
            self.threadings.append(t3)

    def run(self):
        '''
        主程序, 暂时没有运行多线程
        无参数
        :return: None
        '''
        self.get_file_queue()
        self.get_html_queue()
        self.get_positions_queue_from_html()
        self.save_positions_into_txt()


if __name__ == '__main__':
    json_to_txt = JsonToTxt()
    json_to_txt.run()
