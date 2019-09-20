#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   data_clear_by_pandas.py    
@Contact :   zyf.912@163.com
@License :   (C)Copyright 2019-2020, Zyf-FT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/9/18 15:27   zyfei      1.0         None
'''

import pandas
# import matplotlib
# import matplotlib.pyplot as plt


data_columns = ['companyFullName', 'positionName', 'createTime', 'companyShortName', 'city', 'education', 'jobNature', 'salary', 'industryField', 'financeStage', 'positionAdvantage', 'companySize', 'companyLabelList', 'district', 'positionLables']
data_lagou = pandas.read_csv(
                        '../txt/positions_test.csv',
                        header=None,
                        names=data_columns,
                        sep=';',
                        engine='python',
                        error_bad_lines=False,
                        encoding='utf-8',
                         )
# 跳过错误行
# Skipping line 247: Expected 15 fields in line 247, saw 18
# Skipping line 446: Expected 15 fields in line 446, saw 18
# Skipping line 920: Expected 15 fields in line 920, saw 16
# Skipping line 991: Expected 15 fields in line 991, saw 16
# 打印前五行看看
# print(data_lagou.head())
#
print(data_lagou.describe())
# 查看 education 出现的频率
educations = pandas.Series(data_lagou.education)
education_value_counts = educations.value_counts()
print(education_value_counts)
# education_value_counts.plot(kind='bar')

# 处理 salary 列
salaries = pandas.Series(data_lagou.salary)
print(salaries.head())

def str_to_str_into_int(salary):
    salary = salary
    salary_min, salary_max = salary[:-1].split('-')
    salary_min = int(salary_min)
    salary_max = int(salary_max)
    return salary_min, salary_max

