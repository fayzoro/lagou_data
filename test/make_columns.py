#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   make_columns.py    
@Contact :   zyf.912@163.com
@License :   (C)Copyright 2019-2020, Zyf-FT

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/9/18 15:54   zyfei      1.0         None
'''

import re

string = '''
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
'''

pattern = r"position\['(\w*?)'\]"
results = re.findall(pattern, string, flags=0)
print(results)