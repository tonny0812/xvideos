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

from pySmartDL import SmartDL

import SpiderConfig
from Entites.Video import Video
from Utils import RequestUtil


class XVideoDownloader(object):

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

class XNXXVideoDownloader(object):
    def __init__(self):
        self.video = None

    def set_video(self, video):
        self.video = video

    def download_parallel(self):
        file_path = os.path.join(SpiderConfig.VIDEOS_OUTPUT_TEMP_PATH, self.video.get_title())
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        self.download(file_path, self.video.get_title() + '.mp4', self.video.get_url())
        return file_path

    def download(self, parent_path, filename, url):
        obj = SmartDL(url, parent_path)
        obj.start()

if __name__ == "__main__":
    d = XNXXVideoDownloader()
    video = Video('S-Cute', 'https://vid-egc.xnxx-cdn.com/videos/mp4/3/e/a/xvideos.com_3eabfb06537aacf1f8c7ef09022108c3-1.mp4?Sk6tylpHMgUFALI-IFFhxjqKZPedahTPWg1nkkvaBN4QB3tIwJ-27_9Vn4X_m3ekBa3CIHk5roQPLyPtlmUaVg3dsDPLnpR2fNUh49_4y-AoS1MBEihjQvSxvN2B8wpPcoGvs_SoyTslc1S_bzGvYkYZT7VPBL3ilHd0dKVXXILQ2V2rfrkFFs2kB5Wc0YUMK3gdlAjxwiYzwQ&ui=MTcyLjk2LjIxOS41MC0vdmlkZW8taDViMzcyNy9zLWN1dGU=')
    d.set_video(video)
    d.download_parallel()