# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     SpiderConfig
   Description :
   Author :       qiuqiu
   date：          2019/10/22
-------------------------------------------------
"""
import os

# 视频上限
MAX_NUMBER = 1000
VIDEOS_OUTPUT_LIST_FILE_PATH = os.path.join(os.path.dirname(__file__), "文件", "video_list.html")
VIDEOS_OUTPUT_REAL_URL_LIST_FILE_PATH = os.path.join(os.path.dirname(__file__), "文件", "real_video_list.html")
VIDEOS_OUTPUT_TEMP_PATH = os.path.join(os.path.dirname(__file__), "视频", "temp")
VIDEOS_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "视频")

PROXIES = {'http': '127.0.0.1:1080', 'https': '127.0.0.1:1080'}

PARALLEL_NUM = 5

urls = ['https://www.xvideos.com/%s' % n for n in
        [''] + ['new/%d' % m for m in list(range(1, 2))] + ['lang/chinese/%s' % p for p in list(range(1, 3))] +
        ['c/Solo&Masturbation-33'] + ['c/%s/Solo&Masturbation-33' % s for s in list(range(1, 2))]]
