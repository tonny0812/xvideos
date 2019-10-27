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


# 获取需要转换的路径
def get_user_path(argv_dir):
    if os.path.isdir(argv_dir):
        return argv_dir
    elif os.path.isabs(argv_dir):
        return argv_dir
    else:
        return False


# 对转换的TS文件进行排序
def get_sorted_ts(user_path):
    ts_list = glob(os.path.join(user_path, '*.ts'))
    # print(ts_list)
    boxer = []
    for ts in ts_list:
        if os.path.exists(ts):
            # print(os.path.splitext(os.path.basename(ts)))
            file, _ = os.path.splitext(os.path.basename(ts))
            boxer.append(int(file))
    boxer.sort()
    # print(boxer)
    return boxer


# 文件合并
def convert_m3u8(boxer, o_file_name):
    # cmd_arg = str(ts0)+"+"+str(ts1)+" "+o_file_name
    tmp = []
    for ts in boxer:
        tmp.append(str(ts) + '.ts')
    cmd_str = '+'.join(tmp)
    exec_str = "copy /b " + cmd_str + ' ' + o_file_name
    # print("copy /b "+cmd_str+' '+o_file_name)
    os.system(exec_str)


if __name__ == '__main__':
    o_dir = r'C:\Users\qiuqiu\PycharmProjects\xvideos\文件\Who is this girl'
    o_file_name = r'test.mp4'
    # print(o_dir+":"+o_file_name)
    user_path = get_user_path(o_dir)
    print(user_path)
    if not user_path:
        print("您输入的路径不正确，:-(");
    else:
        if os.path.exists(os.path.join(user_path, o_file_name)):
            print('目标文件已存在，程序停止运行。')
            exit(0)
        os.chdir(user_path)
        # convert_m3u8('2.ts','4.ts',o_file_name)
        boxer = get_sorted_ts(user_path)
        convert_m3u8(boxer, o_file_name)
        # print(os.getcwd())
