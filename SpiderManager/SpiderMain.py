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
        # 添加入口URL
        self.manager.add_new_url(root_url)
        # 判断url管理器中是否有新的url，同时判断抓取了多少个url
        while (self.manager.has_new_url() and self.manager.old_url_size() < 1):
            try:
                # 从URL管理器获取新的url
                new_url = self.manager.get_new_url()
                # HTML下载器下载网页
                html = self.downloader.download(new_url)
                # HTML解析器抽取网页数据
                new_urls, data = self.parser.parser(new_url, html)
                print(new_urls, data)
                # 将抽取到url添加到URL管理器中
                self.manager.add_new_urls(new_urls)
                # 数据存储器储存文件
                self.output.store_data(data)
                print("已经抓取%s个链接" % self.manager.old_url_size())
            except Exception as e:
                print("crawl failed", e)
            # 数据存储器将文件输出成指定格式
        self.output.output_html()


if __name__ == "__main__":
    spider_man = SpiderMain()
    spider_man.crawl("https://www.xvideos.com/video51604517/s-cute_fumika_coitus_with_a_girl_who_has_bazongas_-_nanairo.co")