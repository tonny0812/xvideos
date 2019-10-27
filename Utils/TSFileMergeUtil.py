# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     TSFileMerge
   Description :   合并ts文件
   Author :       qiuqiu
   date：          2019/10/22
-------------------------------------------------
"""
import os
from glob import glob


# 对转换的TS文件进行排序
def get_sorted_ts(user_path):
    ts_list = glob(os.path.join(user_path, '*.ts'))
    boxer = []
    for ts in ts_list:
        if os.path.exists(ts):
            file, _ = os.path.splitext(os.path.basename(ts))
            boxer.append(int(file))
    boxer.sort()
    return boxer

# 文件合并
def convert_m3u8(boxer, desc_file_name):
    tmp = []
    for ts in boxer:
        tmp.append(str(ts) + '.ts')
    cmd_str = '+'.join(tmp)
    exec_str = "copy /B " + cmd_str + ' ' + desc_file_name
    print(exec_str)
    os.system(exec_str)
