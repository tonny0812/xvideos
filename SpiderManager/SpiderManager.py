# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     SpiderMain
   Description :  爬虫调度器，首先要对各个模块初始化，然后通过crawl（root_url)，
                  完成流程运转

   Author :       qiuqiu
   date：          2019/10/22
-------------------------------------------------
"""
import datetime
import threading
import time
from multiprocessing import Queue

import SpiderConfig
from DataOutput.DataOutput import DataOutput
from HtmlDownloader.HtmlDownloader import HtmlDownloader
from HtmlDownloader.VideoDownloader import XVideoDownloader
from HtmlParser.HtmlParser import HtmlParser
from HtmlParser.VideoParser import VideoParser
from URLManager.URLManager import UrlManager


class SpiderManager(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.videodownloader = XVideoDownloader()
        self.videoParser = HtmlParser()
        self.tsParser = VideoParser()
        self.output = DataOutput()
        self.video_queue = Queue()
        self.video_download_queue = Queue()

    def run(self):
        threads = []
        t1 = threading.Thread(target=self.start_video_url_crawl)
        t2 = threading.Thread(target=self.start_video_ts_url_crawl)
        t3 = threading.Thread(target=self.start_video_ts_download)
        threads.append(t1)
        threads.append(t2)
        threads.append(t3)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print('all DONE')

    def start_video_url_crawl(self):
        for v_url in SpiderConfig.urls:
            print("开始获取%s上的视频..." % v_url)
            videoes = self._crawl_videoes_url(v_url)
            if videoes:
                for video in videoes:
                    print("将 %s 进入video_queue中...队列个数%s" % (video.get_title(), self.video_queue.qsize()))
                    self.video_queue.put(video)


    def start_video_ts_url_crawl(self):
        while True:
            if self.video_queue.empty():
                time.sleep(1)
            try:
                video = self.video_queue.get()
                print("从video_queue中获取%s..." % video.get_title())
                ts_urls = self._crawl_video_ts_urls(video.get_url())
                video.set_real_url(ts_urls)
                print("将%s进入video_download_queue中..." % video.get_title())
                self.video_download_queue.put(video)
            except Exception as e:
                print(e)

    def start_video_ts_download(self):
        while True:
            if self.video_queue.empty():
                time.sleep(1)
            try:
                _starttime = datetime.datetime.now()
                video = self.video_download_queue.get()
                print("从video_download_queue中获取%s..." % video.get_title())
                # 下载视频并合并
                self.videodownloader.set_video(video)
                ts_temp_path = self.videodownloader.download_parallel()
                desc_path = self.output.mergeTS(video.get_title() + ".ts", ts_temp_path)
                video.set_local_path(desc_path)
                _endtime = datetime.datetime.now()
                _excutetime = (_endtime - _starttime).seconds
                print("已经抓取%s个视频链接(%d秒)" % (self.manager.video_size(), _excutetime))
            except Exception as e:
                print(e)

    def _crawl_videoes_url(self, root_url):
        try:
            _starttime = datetime.datetime.now()
            # HTML下载器下载网页
            html = self.downloader.download_with_proxies(root_url)
            # HTML解析器抽取网页数据
            videos = self.videoParser.parser(root_url, html)
            return videos
        except Exception as e:
            print("crawl failed", e)
            return None

    def _crawl_video_ts_urls(self, videoURL):
        # HTML下载器下载网页
        html_cont = self.downloader.download_with_proxies(videoURL)
        title, m3u8baseurl, m3u8url = self.tsParser.m3u8parser(html_cont)
        m3u8content = self.downloader.download_with_proxies(m3u8url)
        m3u8HighestUrl = self.tsParser.m3u8HighestParser(m3u8baseurl, m3u8content)
        m3u8HighestContent = self.downloader.download_with_proxies(m3u8HighestUrl)
        tslist = self.tsParser.m3u8TSParser(m3u8baseurl, m3u8HighestContent)
        return tslist

    def get_video_queue(self):
        return self.video_queue

    def get_video_download_queue(self):
        return self.video_download_queue
