#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   sql_mingling.py    
@Contact :   625711951@qq.com
@License :   (C)Copyright 2019-2020, Zyf-FT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/9/23 11:33   zyfei      1.0         None
'''

def main():
    sql = '''
    select database();
    show databases;
    use lagou_data_shuju;
    show tables;
    create table if not exists lagou_data_shuju_test2(
      id int primary key auto_increment,
      companyFullName varchar(30),
      positionName varchar(20),
      createTime datetime,
      positionShortName varchar(10),
      education enum('本科', '硕士', '大专', '不限'),
      city varchar(10),
      jobNature enum('全职', '实习', '兼职'),
      industryField varchar(50),
      financeStare varchar(50),
      positionAdvantage varchar(20),
      companySize varchar(20),
      district varchar(20)
    ) character set 'utf8';
    
    alter table lagou_data_shuju_test2 add salary_min int after district;
    alter table lagou_data_shuju_test2 add salary_max int after salary_min;
    desc lagou_data_shuju_test2;
    alter table lagou_data_shuju_test2 change positionShortName companyShortName varchar(10);
alter table lagou_data_shuju_test2 change financeStare financeStage varchar(50);
    '''

if __name__ == '__main__':
    pass