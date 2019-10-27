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
import time

import SpiderConfig
from DataOutput.DataOutput import DataOutput
from Entites.Video import Video
from HtmlDownloader.HtmlDownloader import HtmlDownloader
from HtmlParser.HtmlParser import HtmlParser
from HtmlParser.VideoParser import VideoParser
from URLManager.URLManager import UrlManager


class SpiderManager(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.videoParser = HtmlParser()
        self.tsParser = VideoParser()
        self.output = DataOutput()

    def crawlVideoURL(self, root_url):
        if self.manager.video_size() < SpiderConfig.MAX_NUMBER:
            try:
                # HTML下载器下载网页
                html = self.downloader.download(root_url)
                # HTML解析器抽取网页数据
                videos = self.videoParser.parser(root_url, html)
                for video in videos:
                    _starttime = datetime.datetime.now()
                    vurl = video.get_url()
                    ts_urls = self._crawl_video_ts_urls(vurl)
                    video.set_real_url(ts_urls)
                    # 将抽取到视频信息url添加到URL管理器中
                    self.manager.add_new_video(video)
                    # 数据存储器储存文件
                    self.output.store_data(video)
                    _endtime = datetime.datetime.now()
                    _excutetime = (_endtime - _starttime).seconds
                    print("已经抓取%s个视频链接(%d秒)" % (self.manager.video_size(),_excutetime))
                    time.sleep(2)
            except Exception as e:
                print("crawl failed", e)
        # 数据存储器将文件输出成指定格式
        self.output.output_html()

    def _crawl_video_ts_urls(self, videoURL):
        # HTML下载器下载网页
        html_cont = self.downloader.download(videoURL)
        title, m3u8baseurl, m3u8url = self.tsParser.m3u8parser(html_cont)
        m3u8content = self.downloader.download(m3u8url)
        m3u8HighestUrl = self.tsParser.m3u8HighestParser(m3u8baseurl, m3u8content)
        m3u8HighestContent = self.downloader.download(m3u8HighestUrl)
        tslist = self.tsParser.m3u8TSParser(m3u8baseurl, m3u8HighestContent)
        return tslist

if __name__ == "__main__":
    spider_man = SpiderManager()
    ts_urls = spider_man._crawl_video_ts_urls('https://www.xvideos.com/video51591929/slim_hun_yui_hatano_amazing_sex_and_blowjob_-_more_at_javhd.net')
    for ts_url in ts_urls:
        print(ts_url)