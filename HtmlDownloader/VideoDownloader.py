# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     VideoDownloader
   Description :
   Author :       qiuqiu
   date：          2019/10/27
-------------------------------------------------
"""
import os
import re
from concurrent.futures import wait, ALL_COMPLETED
from concurrent.futures.thread import ThreadPoolExecutor

import SpiderConfig
from Utils import RequestUtil


class VideoDownloader(object):

    def __init__(self):
        self.video = None
        self.count = 0
        self.ts_num = 0
        self.ts_file_list = []

    def set_video(self, video):
        self.video = video
        self.count = 0
        self.ts_num = len(video.get_real_url())
        self.ts_file_list = []

    def download_parallel(self):
        # 线程池
        file_path = os.path.join(SpiderConfig.VIDEOS_OUTPUT_TEMP_PATH, self.video.get_title())
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        with ThreadPoolExecutor(max_workers=SpiderConfig.PARALLEL_NUM) as excutor:
            all_task = [excutor.submit(self.download, file_path, url) for url in self.video.get_real_url()]
            wait(all_task, return_when=ALL_COMPLETED)
        return file_path

    def download(self, parent_path, ts_url):
        re_str = r'hls-\d{3,4}p(?:-[a-zA-Z0-9]{5})?(\d+.ts)'
        # 目前见过两种，相对路径的前缀分别形如hls-720p3.ts， hls-360p-ba36e0.ts
        ts_name = re.search(re_str, ts_url).group(1)
        # ts_content = RequestUtil.download_content(ts_url, proxies=SpiderConfig.PROXIES)
        ts_content = RequestUtil.download_content(ts_url)
        if ts_content:
            ts_path = os.path.join(parent_path, ts_name)
            with open(ts_path, 'wb') as f:
                f.write(ts_content)
                f.flush()
                self.count += 1
                self.ts_file_list.append(ts_path)
            print("\r视频进度：%.2f%%" % (self.count / self.ts_num * 100), end=' ')
