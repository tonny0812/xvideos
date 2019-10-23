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
import SpiderConfig
from DataOutput.DataOutput import DataOutput
from HtmlDownloader.HtmlDownloader import HtmlDownloader
from HtmlParser.HtmlParser import HtmlParser
from URLManager.URLManager import UrlManager


class SpiderMain(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self, root_url):
        if self.manager.video_size() < SpiderConfig.MAX_NUMBER:
            try:
                # HTML下载器下载网页
                html = self.downloader.download(root_url)
                # HTML解析器抽取网页数据
                videos = self.parser.parser(root_url, html)
                # 将抽取到视频信息url添加到URL管理器中
                self.manager.add_new_videos(videos)
                # 数据存储器储存文件
                self.output.store_datas(videos)
                print("已经抓取%s个视频链接" % self.manager.video_size())
            except Exception as e:
                print("crawl failed", e)
        # 数据存储器将文件输出成指定格式
        self.output.output_html()


if __name__ == "__main__":
    spider_man = SpiderMain()

    urls = ['https://www.xvideos.com', 'https://www.xvideos.com/new/1',
            'https://www.xvideos.com/new/2', 'https://www.xvideos.com/new/3',
            'https://www.xvideos.com/new/4', 'https://www.xvideos.com/new/5',
            'https://www.xvideos.com/new/6', 'https://www.xvideos.com/new/7',
            'https://www.xvideos.com/new/8', 'https://www.xvideos.com/new/9',
            'https://www.xvideos.com/new/10', 'https://www.xvideos.com/new/11']
    # for url in urls:
    #     print("开始抓取：", url)
    #     spider_man.crawl(url)
    spider_man.crawl('https://www.xvideos.com/lang/chinese')
