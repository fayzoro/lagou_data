#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   mysql_connect.py
@Contact :   625711951@qq.com
@License :   (C)Copyright 2019-2020, Zyf-FT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/9/23 10:23   zyfei      1.0         None
'''


from pymysql import connect


class MysqlConnect(object):
    '''数据库连接工具'''
    def __init__(self, database, host='localhost',
                 user='root', password='feifei',
                 charset='utf8', port=3306,):
        '''
        初始化数据库链接参数
        :param database: 要连接的数据库
        :param host: 用户主机
        :param user: 用户名
        :param password: 密码
        :param charset: 数据存储格式
        :param port: 端口
        '''
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.charset = charset
        self.port = port

    def open(self):
        '''
        创建一个连接数据库的方法
        :return: None
        '''
        # 创建数据库连接对象
        self.conn = connect(database=self.database, host=self.host, user=self.user, port=self.port, password=self.password, charset=self.charset)
        # 创建游标对象
        self.cur = self.conn.cursor()

    def close(self):
        '''
        关闭数据库连接的方法
        :return: None
        '''
        self.cur.close()
        self.conn.close()

    def work_on_data(self, sql, lst=[]):
        '''
        运行sql语句，插入，删除， 修改等
        :param sql: sql语句
        :param lst: sql语句中需要填入的参数
        :return: None
        '''
        self.open()
        try:
            self.cur.execute(sql, lst)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print('Faild', e)
        else:
            print('True')
        finally:
            self.close()

    def get_all_data(self, sql, lst=[]):
        '''
        查询数据库指定内容，并返回查询结果
        :param sql: sql语句
        :param lst: sql语句中需要添加的参数
        :return: 查询结果
        '''
        self.open()
        self.cur.execute(sql, lst)
        results = self.cur.fetchall()
        self.close()
        return results


if __name__ == '__main__':
    # mysql_connect = MysqlConnect('lagou_data_shuju_test')
    # insert_sql = ''
    # mysql_connect.work_on_data(sql)
    # select_sql = ''
    # results = mysql_connect.get_all_data(sql)
    # print(results)
    pass