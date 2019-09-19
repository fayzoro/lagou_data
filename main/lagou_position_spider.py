import requests
import os
import random
import time
from queue import Queue
from threading import Thread


class LagouPositionSpider(object):
    ''''''
    def __init__(self):
        self.url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
        self.headers = {
            'Accept': 'application/json,text/javascript,*/*;q = 0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '64',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Cookie': 'JSESSIONID=ABAAABAAADEAAFI000317FE9379B19C2EA80513F57ADDF0; WEBTJ-ID=20190904101008-16cfa0949ff393-018bb68b5db152-3f385c06-1049088-16cfa094a00304; X_HTTP_TOKEN=42daf4b72327b2819003657651bf5e71415983ed09; _ga=GA1.2.1092164625.1567563009; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1567563009; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1567563009; user_trace_token=20190904101009-1f239f45-ceb9-11e9-a508-5254005c3644; LGSID=20190904101009-1f23a09d-ceb9-11e9-a508-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGRID=20190904101009-1f23a29e-ceb9-11e9-a508-5254005c3644; LGUID=20190904101009-1f23a311-ceb9-11e9-a508-5254005c3644; _gid=GA1.2.1307405629.1567563009; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_search; SEARCH_ID=cf4e6bb5ff9e4b7b9d19feaaac7b5739',
            'Host': 'www.lagou.com',
            'Origin': 'https: // www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88?labelWords=&fromSearch=true&suginput=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'X-Anit-Forge-Code': '0',
            'X-Anit-Forge-Token': 'None',
            'X-Requested-With':'XMLHttpRequest',
            }
        self.start_num = 1
        self.end_num = 78
        self.params_queue = Queue()
        self.html_queue = Queue()
        self.save_html_dir = '../html/'
        self.threadings = []

    def get_params_queue(self):
        """
        制作各个post请求对应的 params， 放入队列中
        无参数
        :return: None
        """
        for _i in range(self.start_num, self.end_num + 1):
            params = {
                'first': 'true',
                'pn': str(_i),
                'kd': '数据分析师',
            }
            self.params_queue.put(params)

    def get_html_queue(self):
        '''
        获取网页 将网页放入队列中
        无参数
        :return: none
        '''
        while True:
            # 参数队列中都完成后，结束循环
            if self.params_queue.empty():
                break
            # 获取 post 请求参数，获取网页, 放入队列
            params = self.params_queue.get()
            resp = requests.post(self.url, data=params, json=None, headers=self.headers)
            resp.encoding = 'utf-8'
            html = resp.text
            print(html[:70])
            if '您操作太频繁,请稍后再访问' in html[:200]:
                print('ip暂时被封禁, cookie可能失效，请处理再说')
                self.params_queue.task_done()
                break
            msg = (params['pn'], html)
            self.html_queue.put(msg)
            # 设置请求时间间隔，防止ip被封禁
            time.sleep(40 + random.random() * 20)
            self.params_queue.task_done()

    def save_html_to_file(self):
        '''
        将网页依次存入文件中
        无参数
        :return: None
        '''
        while True:
            if self.html_queue.empty():
                break
            # 获取页码和页面内容
            page_num, html = self.html_queue.get()
            # 设置函数名
            file_name = self.save_html_dir + '第' + page_num + '页.html'
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(html)
                print(file_name, '写入成功')
            self.html_queue.task_done()

    def run(self):
        self.get_params_queue()
        self.get_html_queue()
        self.save_html_to_file()



if __name__ == '__main__':
    lagou_position_spider = LagouPositionSpider()
    lagou_position_spider.run()
