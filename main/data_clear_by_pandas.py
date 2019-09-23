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

# import numpy as np
# import sqlalchemy
import pandas


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

jobNatures = pandas.Series(data_lagou.jobNature)
jobNature_value_counts = jobNatures.value_counts()
print(jobNature_value_counts)
# jobNature_value_counts.plot(kind='bar')

# 处理 salary 列
salaries = pandas.Series(data_lagou.salary)
print(salaries.head())

def str_to_str_into_int(salary):
    salary = salary
    salary_min, salary_max = salary.strip().split('-')
    # print(salary_min, salary_max)
    salary_min = int(salary_min[:-1])
    salary_max = int(salary_max[:-1])
    return salary_min, salary_max

bar = np.frompyfunc(str_to_str_into_int, 1, 2)
print(bar)

salary_min, salary_max = bar(salaries)
# print(salary_min, salary_max)

# 将薪资范围调整为 两个字段，一个最小， 一个最大
columns = data_lagou.columns.tolist()
print(columns)
columns.extend(['salary_min', 'salary_max'])
print(columns)
data_lagou.reindex(columns=columns)
data_lagou['salary_min'] = salary_min
data_lagou['salary_max'] = salary_max
print(data_lagou.describe())

cols = list(data_lagou)
cols.insert(4, cols.pop(cols.index('education')))
data_lagou = data_lagou.loc[:, cols]

data_lagou.drop('salary', 1, inplace=True)
data_lagou.drop('companyLabelList', 1, inplace=True)
data_lagou.drop('positionLables', 1, inplace=True)
print(data_lagou.columns.tolist())

data_lagou.to_csv('../txt/position_df.csv', sep=';', header=None, index=None)
